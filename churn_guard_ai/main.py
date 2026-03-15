import os
import sys
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'src'))

try:
    from data_cleaner import clean_customer_data
    from model_trainer import train_and_save_model
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)


def run_project_pipeline():
    print("=" * 50)
    print("CHURN GUARD AI: PIPELINE INITIALIZED")
    print("=" * 50)

    # 1. Load Raw Data
    data_path = os.path.join(BASE_DIR, 'data', 'customer_data.csv')
    if not os.path.exists(data_path):
        print("Error: data/customer_data.csv not found.")
        print("Please run the code from Notebook 01 to generate the dataset first!")
        return

    df = pd.read_csv(data_path)
    print(f"Data Loaded: {len(df)} customer records found.")

    # 2. Pre-processing & Encoding
    print("Encoding categorical features...")
    le = LabelEncoder()
    # We fit the encoder on the contract type (e.g., 'Month-to-Month' -> 0)
    df['contract_type'] = le.fit_transform(df['contract_type'])

    # Save the encoder so the App can use it later
    encoder_path = os.path.join(BASE_DIR, 'models', 'contract_encoder.pkl')
    os.makedirs(os.path.dirname(encoder_path), exist_ok=True)
    joblib.dump(le, encoder_path)
    print(f"Encoder saved to models/contract_encoder.pkl")

    # 3. Clean Data
    df = clean_customer_data(df, encoder_path)

    # 4. Train the Model
    print("Training Random Forest Classifier...")
    accuracy = train_and_save_model(df)

    print("\n" + "=" * 50)
    print(f"PIPELINE SUCCESSFUL!")
    print(f"Model Accuracy: {accuracy:.2%}")
    print(f"To launch the dashboard, run: streamlit run src/app.py")
    print("=" * 50)


if __name__ == "__main__":
    run_project_pipeline()