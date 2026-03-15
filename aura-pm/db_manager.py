import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('aura_industrial.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Table for machine metadata
    conn.execute('''CREATE TABLE IF NOT EXISTS machines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        model TEXT,
        status TEXT DEFAULT 'Stable'
    )''')
    # Table for sensor data
    conn.execute('''CREATE TABLE IF NOT EXISTS telemetry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id INTEGER,
        temperature REAL,
        vibration REAL,
        pressure REAL,
        timestamp DATETIME,
        FOREIGN KEY (machine_id) REFERENCES machines(id)
    )''')
    conn.commit()
    conn.close()

def log_telemetry(machine_id, temp, vib, press):
    conn = get_db_connection()
    conn.execute('''INSERT INTO telemetry (machine_id, temperature, vibration, pressure, timestamp)
                    VALUES (?, ?, ?, ?, ?)''',
                 (machine_id, temp, vib, press, datetime.now()))
    conn.commit()
    conn.close()