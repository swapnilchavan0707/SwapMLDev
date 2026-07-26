"""
Train models for Chhatrapati Sambhajinagar
- If satellite images exist: Train CNN on images
- Else fallback: Train RF on weather features
"""
import os, glob, pickle, re
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Try to use satellite images for CNN
img_files = glob.glob("data/processed/images/*.npy")
labels_path = "data/processed/labels.csv"

if not os.path.exists(labels_path):
    print("Run python src/download.py first")
    exit(1)

df = pd.read_csv(labels_path, parse_dates=['timestamp'])
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
df['month'] = pd.to_datetime(df['timestamp']).dt.month

# --- Model 1: Weather feature model (always works) ---
print("Training RF on weather features...")
X = df[['temperature','humidity','cloud_cover','hour','month']].fillna(0)
y_class = df['condition']
X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=150, random_state=42)
clf.fit(X_train, y_train)
print(f"RF Classifier Accuracy: {clf.score(X_test, y_test):.3f}")

reg = RandomForestRegressor(n_estimators=150, random_state=42)
reg.fit(X_train, df.loc[X_train.index, 'temperature'])
print(f"RF Regressor R2: {reg.score(X_test, df.loc[X_test.index, 'temperature']):.3f}")

os.makedirs("models", exist_ok=True)
pickle.dump(clf, open("models/weather_classifier.pkl","wb"))
pickle.dump(reg, open("models/temp_regressor.pkl","wb"))

# --- Model 2: CNN on satellite images if we have matched pairs ---
if len(img_files) > 10:
    print(f"\nFound {len(img_files)} satellite images, training CNN...")
    try:
        import tensorflow as tf
        # Build matched dataset
        matched_X=[]; matched_y=[]
        for img_path in img_files:
            m = re.search(r'sat_(\d{4})(\d{2})(\d{2})_(\d{1,2})', img_path)
            if not m: continue
            ts = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)))
            closest = df.iloc[(pd.to_datetime(df['timestamp']) - pd.to_datetime(ts).tz_localize('Asia/Kolkata')).abs().argsort()[:1]]
            if closest.empty: continue
            img = np.load(img_path)
            matched_X.append(img)
            matched_y.append(closest.iloc[0]['condition'])
        if len(matched_X) >=10:
            X_img = np.array(matched_X)[..., np.newaxis] # (N,64,64,1)
            y_img = pd.Series(matched_y)
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()
            y_enc = le.fit_transform(y_img)
            pickle.dump(le, open("models/label_encoder.pkl","wb"))
            Xtr, Xte, ytr, yte = train_test_split(X_img, y_enc, test_size=0.2, random_state=42)
            model = tf.keras.Sequential([
                tf.keras.layers.Conv2D(32,3,activation='relu',input_shape=(64,64,1)),
                tf.keras.layers.MaxPool2D(),
                tf.keras.layers.Conv2D(64,3,activation='relu'),
                tf.keras.layers.MaxPool2D(),
                tf.keras.layers.Conv2D(128,3,activation='relu'),
                tf.keras.layers.GlobalAveragePooling2D(),
                tf.keras.layers.Dense(64,activation='relu'),
                tf.keras.layers.Dense(len(le.classes_), activation='softmax')
            ])
            model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            model.fit(Xtr, ytr, validation_data=(Xte,yte), epochs=10, batch_size=8)
            model.save("models/sat_cnn.h5")
            print("Saved CNN to models/sat_cnn.h5")
    except Exception as e:
        print(f"CNN training skipped: {e}")
else:
    print("\nNot enough satellite images for CNN yet. Run download.py with more hours.")
    print("RF models saved and ready for app.py")

print("\nAll models saved in models/")