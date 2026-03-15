import pandas as pd
import joblib
import os
from sklearn.ensemble import IsolationForest


def get_vibration_column(df):
    """Finds if the column is named 'vibration' or 'vibration_level'."""
    if 'vibration_level' in df.columns:
        return 'vibration_level'
    elif 'vibration' in df.columns:
        return 'vibration'
    return None


def train_anomaly_detector(df):
    vib_col = get_vibration_column(df)

    if not vib_col:
        raise KeyError("Could not find 'vibration' or 'vibration_level' in your CSV!")

    features = ['temperature', 'humidity', vib_col]
    X = df[features]

    print(f" Training using features: {features}")

    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)

    MODEL_DIR = os.path.join(os.path.dirname(__file__), '../models')
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, 'anomaly_detector.pkl'))

    return model


def detect_anomalies(df, model):
    vib_col = get_vibration_column(df)
    if model and vib_col:
        features = ['temperature', 'humidity', vib_col]
        df['anomaly_score'] = model.predict(df[features])
        df['is_anomaly'] = df['anomaly_score'].apply(lambda x: True if x == -1 else False)
    else:
        df['is_anomaly'] = False
    return df