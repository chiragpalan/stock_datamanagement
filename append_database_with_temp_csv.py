import sqlite3
import pandas as pd
import os

# Path to your database
db_path = 'nifty50_data.db'  # Replace with the path to your database

# List of tickers and table names (ensure the table names match the CSV file names)
tickers = ["RELIANCE_NS", "TCS_NS", "INFY_NS", "HDFCBANK_NS", "ICICIBANK_NS"]

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Loop through each ticker, read the CSV file, and append to the corresponding table
for ticker in tickers:
    # Read the CSV file into a DataFrame
    csv_file = f"temp_csvs/{ticker}.csv"
    
    if os.path.exists(csv_file):
        data = pd.read_csv(csv_file)
        
        # Check if data is available
        if not data.empty:
            # Append the data to the corresponding table in the database
            data.to_sql(ticker, conn, if_exists='append', index=False)
            print(f"Data from {csv_file} appended to {ticker} table in the database")
        else:
            print(f"No data found in {csv_file}")
    else:
        print(f"CSV file {csv_file} does not exist")

# Close the database connection
conn.close()
