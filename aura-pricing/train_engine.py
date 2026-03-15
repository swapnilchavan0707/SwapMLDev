import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os


def generate_training_data():
    """Generates synthetic market data if no CSV exists."""
    data = {
        'base_cost': [100, 200, 50, 500, 1000, 150, 300, 80],
        'competitor_price': [120, 210, 55, 520, 1100, 140, 310, 95],
        'stock_level': [2, 15, 1, 20, 3, 30, 5, 12],
        'demand_score': [9, 4, 10, 3, 8, 2, 7, 5],
        # Target: The price that historically yielded the highest profit
        'optimal_price': [125, 208, 62, 515, 1150, 138, 325, 92]
    }
    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/pricing_history.csv', index=False)
    print("Market history dataset created.")


def train_pricing_model():
    if not os.path.exists('data/pricing_history.csv'):
        generate_training_data()

    # Load data
    df = pd.read_csv('data/pricing_history.csv')

    # Features (X) and Target (y)
    X = df[['base_cost', 'competitor_price', 'stock_level', 'demand_score']]
    y = df['optimal_price']

    # Initialize and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save the 'Brain'
    os.makedirs('engine/models', exist_ok=True)
    joblib.dump(model, 'engine/models/pricing_model.pkl')
    print("Pricing Intelligence Model trained and saved to engine/models/")


if __name__ == "__main__":
    train_pricing_model()