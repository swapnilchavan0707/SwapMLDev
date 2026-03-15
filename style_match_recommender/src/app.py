import streamlit as st
import pandas as pd
import os
import sys

# Ensure Python can find the recommender module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from recommender import StyleRecommender


# Initialize the engine
@st.cache_resource
def load_engine():
    return StyleRecommender()


try:
    engine = load_engine()
except FileNotFoundError:
    st.error("⚠️ Data files not found. Please run the notebooks first to generate 'vectorized_features.pkl'!")
    st.stop()

# --- UI Setup ---
st.set_page_config(page_title="Style-Match AI", layout="wide")
st.title("👗 Style-Match: AI Personal Stylist")
st.markdown("Select an item from our catalog to find similar styles instantly.")

# --- Sidebar Selection ---
st.sidebar.header("Browse Catalog")
product_names = engine.df['product_name'].tolist()
selected_product_name = st.sidebar.selectbox("Choose a product:", product_names)

# Get details of selected product
selected_row = engine.df[engine.df['product_name'] == selected_product_name].iloc[0]

# --- Main View ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Your Selection")
    st.info(f"**{selected_row['product_name']}**")
    st.write(f"**Category:** {selected_row['category']}")
    st.write(f"**Style:** {selected_row['style']}")
    st.caption(f"Tags: {selected_row['description_tags']}")

with col2:
    st.subheader("Recommended Styles")
    recommendations = engine.get_recommendations(selected_row['product_id'])

    if not recommendations.empty:
        # Display recommendations in a grid
        cols = st.columns(len(recommendations))
        for i, (idx, row) in enumerate(recommendations.iterrows()):
            with cols[i]:
                st.success(row['product_name'])
                st.caption(f"Category: {row['category']}")
                st.caption(f"Style: {row['style']}")
    else:
        st.write("No recommendations found.")

st.divider()
st.caption("Powered by TF-IDF Vectorization and Cosine Similarity.")