import joblib
import os
import pandas as pd


class DemandPredictor:
    def __init__(self):
        self.model_path = 'engine/models/pricing_model.pkl'
        self.model = self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            return joblib.load(self.model_path)
        return None

    def predict_optimal_price(self, base_cost, comp_price, stock, demand_score=5):
        """
        Uses the Random Forest model to predict the most profitable price.
        """
        if not self.model:
            return None

        # Prepare data for prediction
        input_data = pd.DataFrame([{
            'base_cost': base_cost,
            'competitor_price': comp_price,
            'stock_level': stock,
            'demand_score': demand_score
        }])

        prediction = self.model.predict(input_data)
        return round(prediction[0], 2)