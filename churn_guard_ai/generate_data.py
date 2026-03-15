import pandas as pd
import numpy as np
import os


def generate_churn_data(n=1000):
    np.random.seed(42)
    data = {
        'customer_id': range(1, n + 1),
        'tenure_months': np.random.randint(1, 72, n),
        'contract_type': np.random.choice(['Month-to-Month', 'One Year', 'Two Year'], n),
        'monthly_charges': np.random.uniform(20, 120, n),
        'support_tickets': np.random.randint(0, 10, n)
    }
    df = pd.DataFrame(data)
    # Calculate total charges
    df['total_charges'] = df['tenure_months'] * df['monthly_charges']

    # Logic for churn (Target variable)
    # High risk if: Month-to-Month contract AND high support tickets
    churn_logic = (
            (df['contract_type'] == 'Month-to-Month') & (df['support_tickets'] > 5) |
            (df['tenure_months'] < 4)
    )
    df['churn'] = np.where(churn_logic, np.random.choice([0, 1], size=n, p=[0.2, 0.8]),
                           np.random.choice([0, 1], size=n, p=[0.9, 0.1]))

    # Save the file
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/customer_data.csv', index=False)
    print(f"Success! Created 'data/customer_data.csv' with {n} rows.")


if __name__ == "__main__":
    generate_churn_data()