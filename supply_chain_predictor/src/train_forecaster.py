import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'demand_forecaster.pkl')


def train_regression_model(df):
    """
    Trains a Random Forest Regressor to predict units_sold.
    """
    # 1. Create Model Directory if it doesn't exist
    os.makedirs(MODEL_DIR, exist_ok=True)

    # 2. Define Features (X) and Target (y)
    # We include our raw sensors (price/weather) and engineered features (lags)
    features = [
        'price', 'is_promotion', 'weather_score', 'is_weekend',
        'day_of_week', 'month', 'sales_lag_1', 'sales_lag_7', 'rolling_mean_3'
    ]

    X = df[features]
    y = df['units_sold']

    # 3. Split the data
    # In time-series, we usually split by date, but for a simple project,
    # a random split works to evaluate general pattern recognition.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Initialize and Train the Model
    print("Training Demand Forecasting Model (Random Forest Regressor)...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluate the Model
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print("\n--- Model Performance ---")
    print(f"Mean Absolute Error (MAE): {mae:.2f} units")
    print(f"R-squared Score: {r2:.2f}")
    print("-------------------------")

    # 6. Save the Model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    # This block allows us to run training directly for testing
    from data_loader import load_sales_data
    from feature_engineering import create_demand_features

    # Pipeline: Load -> Engineer -> Train
    raw_data = load_sales_data()
    if raw_data is not None:
        enriched_data = create_demand_features(raw_data)
        train_regression_model(enriched_data)