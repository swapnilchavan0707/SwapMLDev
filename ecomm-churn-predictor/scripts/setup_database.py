import sqlite3
import pandas as pd
import numpy as np
import os

# Create directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')


def generate_ecommerce_data():
    # Connect to (or create) the database
    conn = sqlite3.connect('data/ecommerce.db')
    cursor = conn.cursor()

    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            tenure_months INTEGER,
            avg_order_value REAL,
            last_login_days INTEGER,
            complaints_count INTEGER,
            delivery_delay_rate REAL,
            churned INTEGER
        )
    ''')

    # Generate 1,000 rows of synthetic "Real World" data
    np.random.seed(42)  # For consistent results
    n_rows = 1000

    # Feature 1: Tenure (1 to 60 months)
    tenure = np.random.randint(1, 61, n_rows)

    # Feature 2: Avg Order Value ($10 to $500)
    order_val = np.random.uniform(10, 500, n_rows).round(2)

    # Feature 3: Days since last login (0 to 90 days)
    last_login = np.random.randint(0, 91, n_rows)

    # Feature 4: Complaints (0 to 10)
    complaints = np.random.randint(0, 11, n_rows)

    # Feature 5: Delivery Delay Rate (0% to 50%)
    delays = np.random.uniform(0, 0.5, n_rows).round(2)

    # LOGIC FOR CHURN (The "Pattern" the AI will look for)
    # A customer is more likely to churn if:
    # High login days OR high complaints OR many delivery delays
    churn_prob = (last_login / 90) * 0.4 + (complaints / 10) * 0.4 + (delays * 0.2)
    churned = (churn_prob > 0.5).astype(int)

    # Combine into a list of tuples
    data = list(zip(tenure.tolist(), order_val.tolist(), last_login.tolist(),
                    complaints.tolist(), delays.tolist(), churned.tolist()))

    # Insert data into the database
    cursor.executemany('''
        INSERT INTO customers (tenure_months, avg_order_value, last_login_days, 
                               complaints_count, delivery_delay_rate, churned) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)

    conn.commit()

    # Quick check: How many churned?
    print(f"Database created! Total records: {n_rows}")
    print(f"Total churned customers in DB: {sum(churned)}")

    conn.close()


if __name__ == "__main__":
    generate_ecommerce_data()