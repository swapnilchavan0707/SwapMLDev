import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Configuration
MODEL_FILE = 'expiry_model.pkl'


def train_model():
    """
    Trains a simple Random Forest model to predict food shelf life.
    Features: [Category_ID, Storage_ID]
    Categories: 0: Fruit, 1: Dairy, 2: Meat, 3: Vegetables
    Storage: 0: Pantry, 1: Fridge
    """
    # Mock Data: [Category, Storage] -> Days until expiry
    # This represents a simplified dataset of food spoilage patterns
    data = np.array([
        [0, 0, 7],  # Fruit in Pantry -> 7 days
        [0, 1, 14],  # Fruit in Fridge -> 14 days
        [1, 1, 10],  # Dairy in Fridge -> 10 days
        [2, 1, 5],  # Meat in Fridge -> 5 days
        [2, 0, 1],  # Meat in Pantry -> 1 day
        [3, 0, 5],  # Veggies in Pantry -> 5 days
        [3, 1, 12]  # Veggies in Fridge -> 12 days
    ])

    X = data[:, :2]  # Features (Category, Storage)
    y = data[:, 2]  # Target (Days)

    print("Training the Expiry Predictor model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save the model to a file so we don't have to retrain every time
    joblib.dump(model, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")
    return model


def get_model():
    """Loads the model from disk or trains a new one if it doesn't exist."""
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    else:
        return train_model()


def predict_life(category_id, storage_id):
    """
    Takes input from the web frontend and returns a prediction.
    :param category_id: Integer representing the food category
    :param storage_id: Integer representing storage (0 for Pantry, 1 for Fridge)
    :return: Predicted days (Integer)
    """
    model = get_model()

    # Reshape input for scikit-learn (expects 2D array)
    input_data = np.array([[category_id, storage_id]])
    prediction = model.predict(input_data)

    # Return the result as a rounded integer
    return int(np.round(prediction[0]))


if __name__ == "__main__":
    # If run directly, this will train and save the model
    train_model()

    # Test a prediction: Fruit (0) in the Fridge (1)
    test_prediction = predict_life(0, 1)
    print(f"Test Prediction (Fruit in Fridge): {test_prediction} days")