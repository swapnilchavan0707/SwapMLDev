import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import joblib
import os
import sys
from datetime import datetime

# --- PATH FIX ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'src'))
from data_processor import process_sensor_data

# --- CONFIG ---
st.set_page_config(page_title="IoT Smart Logistics", layout="wide")

# CSS: Times New Roman + Icon Fix
st.markdown("""
    <style>
    html, body, [class*="st-"], .stMetric { font-family: 'Times New Roman', Times, serif !important; }
    [data-testid="stExpander"] summary p { margin-left: 10px; font-family: 'Times New Roman' !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD ---
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw_sensor_stream.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'anomaly_detector.pkl')


@st.cache_data
def load_and_clean():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        return process_sensor_data(df)
    return None


df = load_and_clean()
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

# --- UI ---
st.title(" IoT Smart Logistics Tracker")
st.divider()

if df is not None:
    # Latest Status
    latest = df.iloc[-1]

    if model:
        from anomaly_engine import detect_anomalies

        df = detect_anomalies(df, model)
        is_bad = df.iloc[-1]['is_anomaly']
    else:
        is_bad = False

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Temp", f"{latest['temperature']}°C")
    m2.metric("Distance Covered", f"{latest['total_distance']:.2f} km")

    if is_bad:
        m3.error("Status: ANOMALY DETECTED")
    else:
        m3.success("Status: HEALTHY")

    # Map Row
    st.subheader(" Live Shipment Map")
    m = folium.Map(location=[latest['latitude'], latest['longitude']], zoom_start=11)

    # Path Line
    points = df[['latitude', 'longitude']].values.tolist()
    folium.PolyLine(points, color="blue", weight=2).add_to(m)

    # Markers
    for i, row in df.iterrows():
        color = 'red' if row.get('is_anomaly', False) else 'green'
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=4, color=color, fill=True
        ).add_to(m)

    st_folium(m, width=1300, height=500)

    with st.expander(" View Sensor History Log"):
        st.dataframe(df, use_container_width=True)
else:
    st.warning("No data found. Please run main.py first.")