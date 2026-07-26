import os
import sqlite3
import pandas as pd


def setup_database():
    # Define file paths based on the project structure
    csv_path = os.path.join('data', 'raw_weather.csv')
    db_path = os.path.join('data', 'weather_data.db')

    # 1. Check if the raw data file exists
    if not os.path.exists(csv_path):
        print(f"Error: Please place your dataset file at '{csv_path}' first.")
        return

    print("Reading raw weather data...")
    # Load data (handles standard formats, cleans column whitespaces)
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # 2. Connect to SQLite database (creates file if it doesn't exist)
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)

    # 3. Write data to a table named 'india_weather'
    print("Inserting data into 'india_weather' table...")
    df.to_sql('india_weather', conn, if_exists='replace', index=False)

    # Verify insertion
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM india_weather")
    row_count = cursor.fetchone()[0]

    conn.close()
    print(f"Success! Database ready with {row_count} rows loaded.")


if __name__ == "__main__":
    setup_database()
