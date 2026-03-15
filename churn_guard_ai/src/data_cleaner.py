import pandas as pd
import joblib
import os


def clean_customer_data(df, encoder_path):
    """
    Standardizes column names and encodes categorical variables.
    """
    # 1. Ensure columns are consistent
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]

    # 2. Load the LabelEncoder used during training
    if os.path.exists(encoder_path):
        le = joblib.load(encoder_path)
        # Handle cases where new data has 'contract_type' as text
        if 'contract_type' in df.columns and df['contract_type'].dtype == 'object':
            df['contract_type'] = le.transform(df['contract_type'])

    # 3. Handle missing values
    df = df.fillna(0)

    return df


if __name__ == "__main__":
    # Test path
    print("Data cleaner module ready.")