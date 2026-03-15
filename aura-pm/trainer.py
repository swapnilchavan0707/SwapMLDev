import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os


def train_model():
    # 1. Setup paths
    data_dir = 'data'
    model_dir = 'ml_engine/models'
    csv_path = os.path.join(data_dir, 'sensor_data.csv')

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)

    # 2. Create dummy data if CSV doesn't exist
    if not os.path.exists(csv_path):
        data = {
            'temperature': [80, 90, 110, 130, 70, 85, 150],
            'vibration': [1, 3, 5, 10, 0.5, 2, 15],
            'pressure': [30, 35, 45, 60, 25, 32, 80],
            'rul': [150, 100, 50, 10, 200, 120, 1]  # Target: Remaining Days
        }
        pd.DataFrame(data).to_csv(csv_path, index=False)
        print(f"Generated sample data at {csv_path}")

    # 3. Train
    df = pd.read_csv(csv_path)
    X = df[['temperature', 'vibration', 'pressure']]
    y = df['rul']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 4. Save
    joblib.dump(model, os.path.join(model_dir, 'rf_v1.pkl'))
    print("Intelligence model (rf_v1.pkl) successfully saved.")


if __name__ == "__main__":
    train_model()