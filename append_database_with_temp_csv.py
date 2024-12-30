import os
import sqlite3
import pandas as pd

# Path to your database
db_path = "nifty50_data.db"

# List of tickers and corresponding table names
tickers = ["RELIANCE_NS", "TCS_NS", "INFY_NS", "HDFCBANK_NS", "ICICIBANK_NS"]
csv_dir = "temp_csvs"

# Connect to the database
conn = sqlite3.connect(db_path)

for ticker in tickers:
    csv_path = os.path.join(csv_dir, f"{ticker}.csv")
    
    if os.path.exists(csv_path):
        # Read the CSV file
        df = pd.read_csv(csv_path)
        
        # Append the data to the database
        df.to_sql(ticker, conn, if_exists="append", index=False)
        print(f"Appended data from {csv_path} to {ticker} table.")
    else:
        print(f"CSV file {csv_path} does not exist.")

# Close the connection
conn.close()
