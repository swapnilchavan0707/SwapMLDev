import pandas as pd
import os
import sqlite3

# --- PATH SETUP ---
# Locates the data folder relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'sales_history.csv')
DB_PATH = os.path.join(BASE_DIR, 'data', 'inventory.db')

def load_sales_data():
    """
    Loads sales data from CSV, ensures correct data types,
    and sorts by date for time-series analysis.
    """
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return None

    print(f"Loading data from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH)

    # 1. Convert date strings to Datetime objects
    df['date'] = pd.to_datetime(df['date'])

    # 2. Sort by date (Critical for forecasting models)
    df = df.sort_values(by='date').reset_index(drop=True)

    # 3. Basic Cleaning: Fill missing units with 0 (if any)
    df['units_sold'] = df['units_sold'].fillna(0)

    print(f"Loaded {len(df)} rows of sales data.")
    return df

def sync_to_database(df):
    """
    Syncs the current dataframe into a SQLite database
    to simulate a real warehouse inventory system.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        # We save the data to a table called 'historical_demand'
        df.to_sql('historical_demand', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Data synced to SQLite database: {DB_PATH}")
    except Exception as e:
        print(f"Database Sync Error: {e}")

if __name__ == "__main__":
    # Test the loader
    sales_df = load_sales_data()
    if sales_df is not None:
        print(sales_df.head())
        sync_to_database(sales_df)