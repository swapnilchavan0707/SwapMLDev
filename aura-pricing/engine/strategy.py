from engine.demand_model import DemandPredictor

class PricingStrategy:
    def __init__(self):
        self.predictor = DemandPredictor()
        self.min_margin = 0.15 # 15% Profit Floor

    def apply_rules(self, product):
        # 1. Get ML-recommended price
        ml_price = self.predictor.predict_optimal_price(
            product.base_cost,
            product.competitor_price,
            product.stock_level
        )

        # 2. Define the absolute "Floor" price
        floor_price = product.base_cost * (1 + self.min_margin)

        # 3. Decision Logic
        if ml_price:
            # If the ML suggests a price below our profit floor, use the floor
            final_price = max(ml_price, floor_price)
        else:
            # Fallback logic if the ML model isn't trained yet
            final_price = max(product.competitor_price - 0.99, floor_price)

        # 4. Scarcity Override: If stock is critically low, bump price regardless
        if product.stock_level > 0 and product.stock_level < 3:
            final_price *= 1.15

        return round(final_price, 2)