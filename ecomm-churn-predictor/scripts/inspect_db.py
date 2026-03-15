import sqlite3
import pandas as pd

conn = sqlite3.connect('data/ecommerce.db')
# This SQL command fetches the top 5 most "at risk" customers
query = "SELECT * FROM customers WHERE churned = 1 LIMIT 5"
df = pd.read_sql(query, conn)

print("--- Samples of customers who might leave ---")
print(df)
conn.close()