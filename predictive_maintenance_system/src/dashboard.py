import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import numpy as np

# --- 1. DYNAMIC PATH SETUP ---
# Ensures the dashboard finds files whether run from /src or the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'maintenance.db')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'failure_model.pkl')


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_data():
    """Fetch all records from SQLite sensor_logs table."""
    conn = get_connection()
    query = "SELECT * FROM sensor_logs ORDER BY timestamp DESC"
    df = pd.read_sql(query, conn)
    conn.close()
    # Convert timestamp to datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Create a readable status label
    df['Status'] = df['target'].map({0: 'Healthy', 1: 'Failure'})
    return df


# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Predictive Maintenance",
    page_icon="🔧",
    layout="wide"
)

# --- 3. SIDEBAR: REAL-TIME AI INFERENCE ---
st.sidebar.header("Live AI Prediction")
st.sidebar.markdown("Use the sliders to simulate real-time sensor input and test the ML model.")

input_temp = st.sidebar.slider("Temperature (°C)", 40, 110, 70)
input_vib = st.sidebar.slider("Vibration (Hz)", 5, 35, 15)
input_pres = st.sidebar.slider("Pressure (PSI)", 50, 160, 100)

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    # Model expects: [[temperature, vibration, pressure]]
    features = np.array([[input_temp, input_vib, input_pres]])
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    st.sidebar.divider()
    if prediction == 1:
        st.sidebar.error(f" **FAILURE RISK: {probability * 100:.1f}%**")
        st.sidebar.warning("Action Required: Schedule immediate maintenance.")
    else:
        st.sidebar.success(f"**SYSTEM HEALTHY ({(1 - probability) * 100:.1f}%)**")
        st.sidebar.info("System operating within normal parameters.")
else:
    st.sidebar.warning("Model file (`failure_model.pkl`) not found in `/models`. Please run `train_model.py`.")

# --- 4. MAIN DASHBOARD UI ---
st.title("Predictive Maintenance Dashboard")
st.markdown(f"**Data Source:** `SQLite Database` | **Status:** Connected")

if os.path.exists(DB_PATH):
    df = load_data()

    # --- ROW 1: KEY PERFORMANCE INDICATORS (KPIs) ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric("Total Logs", len(df))
    with kpi2:
        avg_vib = df['vibration'].mean()
        st.metric("Avg Vibration", f"{avg_vib:.2f} Hz")
    with kpi3:
        avg_temp = df['temperature'].mean()
        st.metric("Avg Temp", f"{avg_temp:.2f} °C")
    with kpi4:
        failure_count = df[df['target'] == 1].shape[0]
        st.metric("Total Failures", failure_count, delta="- Critical Issues", delta_color="inverse")

    st.divider()

    # --- ROW 2: INTERACTIVE ANALYTICS ---
    col_graph, col_corr = st.columns([2, 1])

    with col_graph:
        st.subheader("Vibration Trends & Failure Events")
        fig_timeline = px.scatter(
            df, x='timestamp', y='vibration',
            color='Status',
            color_discrete_map={'Healthy': '#3498db', 'Failure': '#e74c3c'},
            hover_data=['temperature', 'pressure'],
            title="Vibration Over Time (Click legend to filter)"
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

    with col_corr:
        st.subheader("Feature Correlation")
        # Only correlate numeric columns
        corr_matrix = df[['temperature', 'vibration', 'pressure', 'target']].corr()
        fig_heat = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale='RdBu_r',
            title="Correlation Matrix"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # --- ROW 3: DISTRIBUTION EXPLORER ---
    st.divider()
    st.subheader("Sensor Distribution Analysis")
    target_sensor = st.selectbox("Select Sensor for Box Plot Analysis:", ['temperature', 'vibration', 'pressure'])

    fig_box = px.box(
        df, x="Status", y=target_sensor,
        color="Status",
        points="all",
        color_discrete_map={'Healthy': '#3498db', 'Failure': '#e74c3c'},
        title=f"{target_sensor.capitalize()} Spread: Healthy vs. Failure"
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # --- ROW 4: DATA TABLE ---
    with st.expander("View Raw SQLite Records"):
        st.dataframe(df.drop(columns=['Status']), use_container_width=True)

else:
    st.error(f"CRITICAL ERROR: Database not found at {DB_PATH}. Please ensure `database_manager.py` has been executed.")