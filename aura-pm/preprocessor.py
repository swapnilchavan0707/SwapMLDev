import pandas as pd
import numpy as np


def prepare_features(data_list):
    """
    Standardizes and cleans raw sensor data for the ML model.

    Args:
        data_list (list): A list containing a dictionary of sensor readings.
                         Example: [{'temperature': 95.2, 'vibration': 3.1, 'pressure': 34.0}]

    Returns:
        pd.DataFrame: A cleaned DataFrame ready for model.predict()
    """
    # 1. Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(data_list)

    # 2. Feature Selection
    # We must ensure the columns match the exact order used during training
    required_features = ['temperature', 'vibration', 'pressure']

    # Ensure all required columns exist, if not, create them with 0
    for col in required_features:
        if col not in df.columns:
            df[col] = 0.0

    # 3. Data Cleaning (Imputation)
    # If a sensor sends a null value, we fill it with 0 to prevent ML errors
    df_final = df[required_features].fillna(0)

    # 4. Optional: Feature Engineering (Advanced)
    # In professional PM, we often add "Interaction Terms"
    # Example: vibration divided by pressure can indicate a specific type of wear
    # df_final['vib_press_ratio'] = df_final['vibration'] / (df_final['pressure'] + 1e-6)

    return df_final


if __name__ == "__main__":
    # Test block to verify the preprocessor works independently
    test_data = [{'temperature': 100, 'vibration': 5, 'pressure': 40}]
    processed = prepare_features(test_data)
    print("Processed Data Frame:")
    print(processed)
    print("\nShape:", processed.shape)