import os
import sqlite3
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_weather_model():
    # 1. Define paths and ensure folders exist
    db_path = os.path.join('data', 'weather_data.db')
    model_dir = os.path.join('outputs', 'models')
    os.makedirs(model_dir, exist_ok=True)

    if not os.path.exists(db_path):
        print(f"Error: Database not found at '{db_path}'. Run db_setup.py first.")
        return

    # 2. Extract operational dataset from SQLite database
    print("Extracting data for Machine Learning model...")
    conn = sqlite3.connect(db_path)
    query = "SELECT City, Temperature, Humidity, WindSpeed, Rainfall FROM india_weather"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 3. Preprocessing: Convert Categorical text (City) into Numeric data (One-Hot Encoding)
    print("Preprocessing data and extracting features...")
    df_encoded = pd.get_dummies(df, columns=['City'], drop_first=True)

    # Separate features (X) and target variable (y - predicting Rainfall)
    X = df_encoded.drop(columns=['Rainfall'])
    y = df_encoded['Rainfall']

    # 4. Split data into Training set (80%) and Testing set (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Initialize and Train the Random Forest Regressor
    print("Training Random Forest Regressor Model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)

    # 6. Evaluate Model Performance
    print("Evaluating model performance on test dataset...")
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\n================== MODEL PERFORMANCE METRICS ==================")
    print(f" Mean Absolute Error (MAE) : {mae:.2f} mm")
    print(f" Root Mean Squared Error (RMSE): {rmse:.2f} mm")
    print(f" R-squared Score (R2)          : {r2:.2f}")
    print("===============================================================\n")

    # 7. Save the trained model file for later deployment
    model_path = os.path.join(model_dir, 'weather_predictor.pkl')
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    print(f"Success! Trained model file safely saved to: {model_path}")

    # 8. Showcase a sample dynamic forecast prediction
    print("\n--- Running a sample weather forecast prediction ---")
    # Generating dummy feature structure matching the training data shape
    sample_data = pd.DataFrame([{
        'Temperature': 31.5,
        'Humidity': 82.0,
        'WindSpeed': 14.5,
        **{col: False for col in X.columns if col.startswith('City_')}
    }])

    # Simulating the prediction for Mumbai if it was part of the columns
    if 'City_Mumbai' in sample_data.columns:
        sample_data['City_Mumbai'] = True

    # Reorder columns to exactly match training feature matrix
    sample_data = sample_data[X.columns]

    predicted_rain = model.predict(sample_data)[0]
    print(f"Inputs: Temp=31.5°C, Humidity=82%, Wind=14.5 km/h (City: Mumbai)")
    print(f"Forecasted Rainfall Output: {predicted_rain:.2f} mm")


if __name__ == "__main__":
    train_weather_model()
