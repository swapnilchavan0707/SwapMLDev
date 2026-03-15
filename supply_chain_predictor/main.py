import os
import sys

# Ensure the script can see the 'src' folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import load_sales_data, sync_to_database
from src.feature_engineering import create_demand_features
from src.train_forecaster import train_regression_model


def run_pipeline():
    print("Initializing Supply Chain Forecasting Pipeline")
    print("=" * 50)

    # 1. Load Raw Data
    # Reads from data/sales_history.csv
    raw_df = load_sales_data()

    if raw_df is None:
        print("Pipeline stopped: Could not load raw data.")
        return

    # 2. Sync to SQLite
    # Keeps your inventory database updated for the dashboard
    sync_to_database(raw_df)

    # 3. Feature Engineering
    # Creates Lags, Rolling Averages, and Weekend flags
    print("\n Performing Feature Engineering...")
    enriched_df = create_demand_features(raw_df)

    # 4. Train the ML Model
    # Trains the Regressor and saves demand_forecaster.pkl
    print("\n Training the Demand Forecasting Model...")
    train_regression_model(enriched_df)

    print("\n" + "=" * 50)
    print("SUCCESS: Pipeline completed!")
    print("You can now launch the dashboard using:")
    print("streamlit run src/app.py")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()