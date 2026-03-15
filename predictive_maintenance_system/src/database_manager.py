import sqlite3
import os
import pandas as pd

# --- PATH SETUP ---
# This finds the project root (one level up from /src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'maintenance.db')
CSV_PATH = os.path.join(BASE_DIR, 'data', 'raw_sensors.csv')


def initialize_db():
    """Creates the database and the necessary tables."""
    # Ensure the 'data' folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create Sensor Logs Table (Main Data)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            machine_id TEXT,
            temperature REAL,
            vibration REAL,
            pressure REAL,
            target INTEGER
        )
    ''')

    # 2. Create Maintenance Events Table (Relational structure)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            machine_id TEXT,
            failure_observed INTEGER 
        )
    ''')

    conn.commit()
    print(f"Database initialized at: {DB_PATH}")
    return conn


def import_csv_to_sql(conn):
    """Reads the raw_sensors.csv and populates the SQLite tables."""
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        print("Please ensure you have saved your 'raw_sensors.csv' in the data folder.")
        return

    # Read the CSV
    df = pd.read_csv(CSV_PATH)

    # Convert timestamp column to actual datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 1. Load the full dataset into sensor_logs
    # We use 'replace' so that if you run this script again, it refreshes the data
    df.to_sql('sensor_logs', conn, if_exists='replace', index=False)

    # 2. Extract only the failure rows for the maintenance_events table
    failures = df[df['target'] == 1][['timestamp', 'machine_id', 'target']]
    failures.columns = ['timestamp', 'machine_id', 'failure_observed']  # Rename for schema
    failures.to_sql('maintenance_events', conn, if_exists='replace', index=False)

    print(f"Successfully imported {len(df)} rows to 'sensor_logs'.")
    print(f"Found and logged {len(failures)} failure events in 'maintenance_events'.")


if __name__ == "__main__":
    # Execute the workflow
    connection = initialize_db()
    import_csv_to_sql(connection)
    connection.close()
    print("Database Setup Complete! You can now run the dashboard.")