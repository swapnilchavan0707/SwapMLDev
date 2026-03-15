import sqlite3
import os

# Configuration
DATABASE_NAME = 'smart_shelf.db'

def get_db_connection():
    """
    Returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(drop_existing=False):
    """
    Initializes the database and creates the necessary tables.
    :param drop_existing: If True, deletes existing tables before creating new ones.
    """
    if not os.path.exists(DATABASE_NAME):
        print(f"Creating {DATABASE_NAME}...")

    conn = get_db_connection()
    cursor = conn.cursor()

    if drop_existing:
        print("Dropping existing tables...")
        cursor.execute('DROP TABLE IF EXISTS inventory')

    # Create the inventory table
    # item_name: The name of the grocery
    # category: The food group (Fruit, Dairy, Meat, etc.)
    # date_added: Automatically defaults to the current timestamp
    # predicted_expiry: The integer result from your ML model (days)
    # status: Track if the item is 'Fresh', 'Expiring Soon', or 'Expired'
    print("Creating 'inventory' table...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            predicted_expiry INTEGER NOT NULL,
            status TEXT DEFAULT 'Fresh'
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialization complete.")

if __name__ == "__main__":
    # Running this file directly will initialize the DB.
    # Change to True if you want to wipe the data and start over.
    init_db(drop_existing=False)