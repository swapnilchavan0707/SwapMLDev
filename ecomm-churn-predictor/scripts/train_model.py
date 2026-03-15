import sqlite3
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Ensure the models directory exists
if not os.path.exists('models'):
    os.makedirs('models')

def train_churn_model():
    # 1. Connect to Database
    conn = sqlite3.connect('data/ecommerce.db')
    df = pd.read_sql("SELECT * FROM customers", conn)
    conn.close()

    # 2. Prepare Features and Target
    # We remove 'customer_id' because it's just a label, not a behavior
    X = df.drop(['customer_id', 'churned'], axis=1)
    y = df['churned']

    # 3. Split into Train and Test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Train the Model
    print("Training the Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluate Performance
    y_pred = model.predict(X_test)
    print("\nModel Performance Report:")
    print(classification_report(y_test, y_pred))

    # 6. Save the trained model to a file
    import joblib
    joblib.dump(model, 'models/churn_model.pkl')
    print("\nModel saved to 'models/churn_model.pkl'")

if __name__ == "__main__":
    train_churn_model()