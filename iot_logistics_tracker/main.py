import os
import sys
import pandas as pd

# --- PATH FIX ---
# This ensures Python looks inside the 'src' folder for your modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src'))

try:
    from data_processor import process_sensor_data
    from anomaly_engine import train_anomaly_detector, detect_anomalies
except ImportError as e:
    print(f" Import Error: {e}")
    print("Ensure your files are named correctly in the 'src' folder.")
    sys.exit(1)


def run_pipeline():
    print("=" * 50)
    print(" IOT LOGISTICS PIPELINE: STARTING")
    print("=" * 50)

    # 1. Load Data
    data_path = os.path.join(BASE_DIR, 'data', 'raw_sensor_stream.csv')
    if not os.path.exists(data_path):
        print(f" Error: {data_path} not found.")
        return

    raw_df = pd.read_csv(data_path)
    print(f" Data Loaded: {len(raw_df)} sensor pings.")

    # 2. Process Data
    processed_df = process_sensor_data(raw_df)
    print(f" Metrics Calculated: {processed_df['total_distance'].max():.2f} km traveled.")

    # 3. Train AI
    print("\n Training Anomaly Detection Engine...")
    model = train_anomaly_detector(processed_df)

    # 4. Final Check
    final_df = detect_anomalies(processed_df, model)
    anomalies = final_df[final_df['is_anomaly'] == True]

    print(f" Analysis Complete: Found {len(anomalies)} anomalies.")
    print("=" * 50)
    print("DONE! Run: streamlit run src/app.py")


if __name__ == "__main__":
    run_pipeline()