import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px
from datetime import datetime

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'sales_history_cleaned.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'demand_forecaster.pkl')

# --- PAGE CONFIG ---
st.set_page_config(page_title="Supply Chain Demand AI", layout="wide", page_icon="📦")

# --- CLEAN UI & TARGETED FONT CUSTOMIZATION ---
st.markdown(
    """
    <style>
    /* Apply Times New Roman only to text elements, avoiding icons */
    html, body, .stMarkdown, h1, h2, h3, h4, h5, h6, p, label, .stMetric {
        font-family: 'Times New Roman', Times, serif !important;
    }

    /* Fix for the Expander overlap (preventing font override on icons) */
    [data-testid="stExpander"] summary p {
        font-family: 'Times New Roman', Times, serif !important;
        margin-left: 0.5rem; /* Adds space between icon and text */
    }

    /* Padding for better spacing */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Ensure Metrics don't overlap labels */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-family: 'Times New Roman', Times, serif !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- LOAD DATA & MODEL ---
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH): return None
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    return df


def load_model():
    if os.path.exists(MODEL_PATH): return joblib.load(MODEL_PATH)
    return None


df = load_data()
model = load_model()

# --- HEADER ---
st.title("📦 Supply Chain Demand Forecaster")
st.write("Predictive analytics for inventory optimization.")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("Demand Simulator")
    sim_price = st.slider("Price ($)", 10.0, 30.0, 19.99)
    sim_promo = st.selectbox("Promotion Active?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    sim_weather = st.slider("Weather Score", 1, 10, 7)
    sim_weekend = st.toggle("Is it a Weekend?")

    if model and df is not None:
        now = datetime.now()
        last_known = df['units_sold'].iloc[-1]

        input_dict = {
            'price': [sim_price], 'is_promotion': [sim_promo], 'weather_score': [sim_weather],
            'is_weekend': [int(sim_weekend)], 'day_of_week': [now.weekday()], 'month': [now.month],
            'sales_lag_1': [last_known], 'sales_lag_7': [df['units_sold'].iloc[-7] if len(df) >= 7 else last_known],
            'rolling_mean_3': [df['units_sold'].tail(3).mean()]
        }

        feature_order = ['price', 'is_promotion', 'weather_score', 'is_weekend', 'day_of_week', 'month', 'sales_lag_1',
                         'sales_lag_7', 'rolling_mean_3']
        input_data = pd.DataFrame(input_dict)[feature_order]
        prediction = model.predict(input_data)[0]

        st.divider()
        st.metric("Predicted Demand", f"{int(prediction)} Units")

# --- DASHBOARD CONTENT ---
if df is not None:
    avg_sales = df['units_sold'].tail(7).mean()
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Stock", "450 Units")
    m2.metric("Daily Burn Rate", f"{int(avg_sales)} Units")
    m3.success("Inventory Level: Healthy")

    st.divider()

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Historical Sales")
        fig = px.line(df, x='date', y='units_sold', template="plotly_white")
        fig.update_layout(font_family="Times New Roman", margin=dict(t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Price Analysis")
        fig2 = px.scatter(df, x='price', y='units_sold', color='is_promotion', template="plotly_white")
        fig2.update_layout(font_family="Times New Roman", margin=dict(t=30, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Fixed Expander Section
    with st.expander("View Raw Data History"):
        st.dataframe(df, use_container_width=True)
else:
    st.error("Missing data. Please run main.py.")