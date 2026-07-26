import os
import sqlite3
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


def train_aqi_model():
    db_path = os.path.join('data', 'aqi_data.db')
    model_dir = os.path.join('outputs', 'models')
    os.makedirs(model_dir, exist_ok=True)

    if not os.path.exists(db_path):
        print(f"Error: Database not found at '{db_path}'. Run db_setup.py first.")
        return

    # FIXED: Wrapped PM2.5 in square brackets so SQL handles the dot safely
    print("Extracting data for Machine Learning model...")
    conn = sqlite3.connect(db_path)
    query = "SELECT City, [PM2.5], PM10, NO2, SO2, AQI FROM india_aqi"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 3. Preprocessing: Convert Categorical text (City) into Numeric data
    print("Preprocessing data and extracting features...")
    df_encoded = pd.get_dummies(df, columns=['City'], drop_first=True)

    X = df_encoded.drop(columns=['AQI'])
    y = df_encoded['AQI']

    # 4. Split data into Training set (80%) and Testing set (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Initialize and Train the Random Forest Regressor
    print("Training AQI prediction intelligence engine...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6. Evaluate Model Performance
    y_pred = model.predict(X_test)
    print("\n--- Model Validation Evaluation Metrics ---")
    print(f"Mean Absolute Error (MAE): {mean_absolute_error(y_test, y_pred):.2f} AQI Points")
    print(f"R-squared Engine Score (R2): {r2_score(y_test, y_pred):.2f}")

    # 7. Save the trained model file
    model_path = os.path.join(model_dir, 'aqi_predictor.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nSuccess! Model saved successfully inside: {model_path}")


if __name__ == "__main__":
    train_aqi_model()