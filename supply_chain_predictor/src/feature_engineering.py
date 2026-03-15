import pandas as pd
import numpy as np
import os


def create_demand_features(df):
    """
    Transforms raw sales data into a feature set suitable for ML.
    Creates Lags, Rolling Windows, and Time-based features.
    """
    # 1. Ensure data is sorted by date for time-series logic
    df = df.sort_values('date').reset_index(drop=True)

    # --- TIME FEATURES ---
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

    # --- LAG FEATURES ---
    df['sales_lag_1'] = df['units_sold'].shift(1)
    df['sales_lag_7'] = df['units_sold'].shift(7)

    # --- ROLLING WINDOW FEATURES ---
    df['rolling_mean_3'] = df['units_sold'].shift(1).rolling(window=3).mean()

    # --- PRICE CHANGE ---
    df['price_diff'] = df['price'].diff()

    # 2. Handle missing values created by shifting/rolling
    df = df.dropna().reset_index(drop=True)

    # --- SAVE LOGIC (The Missing Part) ---
    # Get absolute path to the data folder
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_path = os.path.join(BASE_DIR, 'data', 'sales_history_cleaned.csv')

    # Save the dataframe to the data folder
    df.to_csv(processed_path, index=False)

    print(f"Success! Cleaned data saved to: {processed_path}")
    print(f"Feature Engineering Complete. New shape: {df.shape}")

    return df


if __name__ == "__main__":
    from data_loader import load_sales_data

    raw_df = load_sales_data()
    if raw_df is not None:
        enriched_df = create_demand_features(raw_df)
        print("\n--- Enriched Data Preview ---")
        print(enriched_df[['date', 'units_sold', 'sales_lag_1', 'rolling_mean_3']].head())