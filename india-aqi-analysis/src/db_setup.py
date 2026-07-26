import os
import sqlite3
import pandas as pd


def setup_aqi_database():
    csv_path = os.path.join('data', 'raw_aqi.csv')
    db_path = os.path.join('data', 'aqi_data.db')

    if not os.path.exists(csv_path):
        print("Error: data/raw_aqi.csv missing.")
        return

    print("Loading data frame...")
    df = pd.read_csv(csv_path)

    print(f"Connecting to SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)
    df.to_sql('india_aqi', conn, if_exists='replace', index=False)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM india_aqi")
    print(f"Database successfully loaded with {cursor.fetchone()[0]} air quality records.")
    conn.close()


if __name__ == "__main__":
    setup_aqi_database()
