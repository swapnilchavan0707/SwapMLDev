import streamlit as st
import pandas as pd
import joblib
import os
import sys

# Path Fix
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'src'))

# Load Model and Encoder
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'churn_classifier.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'models', 'contract_encoder.pkl')

st.set_page_config(page_title="Churn Guard AI", layout="centered")

# Custom Styling
st.markdown("""
    <style>
    * { font-family: 'Times New Roman', serif; }
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Churn Guard: Customer Retention AI")
st.write("Predict the likelihood of a customer leaving based on usage patterns.")

if not os.path.exists(MODEL_PATH):
    st.error("Model file not found. Please run main.py first to train the AI.")
else:
    model = joblib.load(MODEL_PATH)
    le = joblib.load(ENCODER_PATH)

    with st.form("prediction_form"):
        st.subheader("Customer Details")
        col1, col2 = st.columns(2)

        with col1:
            tenure = st.slider("Tenure (Months)", 1, 72, 12)
            contract = st.selectbox("Contract Type", le.classes_)
            tickets = st.number_input("Support Tickets", 0, 20, 2)

        with col2:
            monthly = st.number_input("Monthly Charges ($)", 20.0, 150.0, 50.0)
            total = tenure * monthly
            st.info(f"Estimated Total Charges: ${total:.2f}")

        submit = st.form_submit_button("Analyze Risk")

    if submit:
        # Prepare input for model
        contract_encoded = le.transform([contract])[0]
        input_data = pd.DataFrame([[tenure, contract_encoded, monthly, total, tickets]],
                                  columns=['tenure_months', 'contract_type', 'monthly_charges', 'total_charges',
                                           'support_tickets'])

        # Predict Probability
        prob = model.predict_proba(input_data)[0][1]  # Probability of Class 1 (Churn)

        st.divider()
        st.subheader("Risk Analysis Result")

        if prob > 0.7:
            st.error(f"HIGH RISK: {prob:.1%} chance of churning.")
            st.warning("Recommendation: Offer a loyalty discount or a 1-year contract extension.")
        elif prob > 0.4:
            st.warning(f"MEDIUM RISK: {prob:.1%} chance of churning.")
            st.info("Recommendation: Send a satisfaction survey.")
        else:
            st.success(f"LOW RISK: {prob:.1%} chance of churning.")
            st.write("Customer appears satisfied.")