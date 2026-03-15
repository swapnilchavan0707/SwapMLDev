import joblib
import pandas as pd


def predict_customer_churn():
    # 1. Load the saved "Brain"
    try:
        model = joblib.load('models/churn_model.pkl')
    except FileNotFoundError:
        print("Error: Model file not found. Run train_model.py first!")
        return

    # 2. Input New Customer Data
    # Format: [tenure_months, avg_order_value, last_login_days, complaints_count, delivery_delay_rate]
    print("\n--- New Customer Churn Risk Analysis ---")

    # Let's simulate a high-risk customer
    new_customer = {
        'tenure_months': 12,
        'avg_order_value': 50.0,
        'last_login_days': 45,  # Hasn't logged in for over a month
        'complaints_count': 8,  # Lots of complaints
        'delivery_delay_rate': 0.4  # 40% of their orders were late
    }

    # Convert to DataFrame for the model
    new_df = pd.DataFrame([new_customer])

    # 3. Make Prediction
    prediction = model.predict(new_df)
    probability = model.predict_proba(new_df)[0][1]  # Probability of Churning

    # 4. Output Result
    print(f"\nAnalysis Result for Customer:")
    if prediction[0] == 1:
        print(f"STATUS: HIGH RISK (Probability: {probability * 100:.1f}%)")
        print("ACTION: Send a retention discount code immediately.")
    else:
        print(f"STATUS: LOW RISK (Probability: {probability * 100:.1f}%)")
        print("ACTION: Maintain standard marketing.")


if __name__ == "__main__":
    predict_customer_churn()