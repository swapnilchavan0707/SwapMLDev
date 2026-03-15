import sqlite3
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'maintenance.db')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'failure_model.pkl')


def train_predictive_model():
    """Extracts data from SQLite, trains the ML model, and saves it."""

    # 1. Ensure the models directory exists
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    # 2. Load Data from SQLite
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}. Run database_manager.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    # We select our features (Temp, Vib, Pres) and our label (Target)
    query = "SELECT temperature, vibration, pressure, target FROM sensor_logs"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("Error: The database table is empty. Check your CSV import.")
        return

    # 3. Feature Selection
    X = df[['temperature', 'vibration', 'pressure']]
    y = df['target']

    # 4. Split Data (80% Training, 20% Testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5. Initialize and Train the Model
    # Random Forest is excellent for sensor data patterns
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6. Evaluate the Model
    y_pred = model.predict(X_test)
    print("\n--- Model Performance Report ---")
    print(classification_report(y_test, y_pred))

    # 7. Save the Model to Disk
    joblib.dump(model, MODEL_PATH)
    print(f"\n Model successfully saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_predictive_model()