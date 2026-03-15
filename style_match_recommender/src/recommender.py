import pandas as pd
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity


class StyleRecommender:
    def __init__(self):
        # Set up paths relative to this file
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.catalog_path = os.path.join(self.base_dir, 'data', 'product_catalog.csv')
        self.vector_path = os.path.join(self.base_dir, 'data', 'vectorized_features.pkl')

        # Load the data
        self.df = pd.read_csv(self.catalog_path)
        self.tfidf_matrix = joblib.load(self.vector_path)

        # Pre-calculate similarity scores for speed
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_recommendations(self, product_id, top_n=4):
        """Finds products most similar to the given product_id."""
        try:
            # Find index of the product
            idx = self.df[self.df['product_id'] == product_id].index[0]

            # Get similarity scores
            sim_scores = list(enumerate(self.cosine_sim[idx]))

            # Sort by score (descending), skipping the first one (itself)
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            top_matches = sim_scores[1:top_n + 1]

            # Return product details
            return self.df.iloc[[i for i, score in top_matches]]
        except Exception as e:
            print(f"Error finding recommendations: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    engine = StyleRecommender()
    print("Recommender Engine Loaded Successfully.")