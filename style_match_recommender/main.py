import os
import sys
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')


def run_style_pipeline():
    print("=" * 50)
    print("STYLE-MATCH AI: PIPELINE INITIALIZED")
    print("=" * 50)

    # 1. Check for Data
    catalog_path = os.path.join(DATA_DIR, 'product_catalog.csv')
    if not os.path.exists(catalog_path):
        print("Error: data/product_catalog.csv not found.")
        print("Please run 'python generate_catalog.py' first!")
        return

    # 2. Load Catalog
    df = pd.read_csv(catalog_path)
    print(f"Catalog Loaded: {len(df)} products ready for vectorization.")

    # 3. Vectorization (The AI "Reading" Phase)
    print("Converting text descriptions into mathematical vectors...")
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['description_tags'].fillna(''))

    # 4. Save the "Brain" (Models and Features)
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Save the Transformer (so the app knows the 'dictionary' used)
    joblib.dump(tfidf, os.path.join(MODEL_DIR, 'tfidf_transformer.pkl'))

    # Save the Matrix (the actual coordinates of each product)
    joblib.dump(tfidf_matrix, os.path.join(DATA_DIR, 'vectorized_features.pkl'))

    print("Vectorized features saved to: data/vectorized_features.pkl")
    print("TF-IDF model saved to: models/tfidf_transformer.pkl")

    print("\n" + "=" * 50)
    print(f"PIPELINE SUCCESSFUL!")
    print(f"To launch your fashion store, run: streamlit run src/app.py")
    print("=" * 50)


if __name__ == "__main__":
    run_style_pipeline()