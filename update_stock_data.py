import sqlite3
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import subprocess

# Database path in the GitHub repository
DB_PATH = "database/nifty50_stocks.db"
STOCK_LIST = [
    "RELIANCE.BO", "TCS.BO", "HDFCBANK.BO", "INFY.BO", "ICICIBANK.BO"  # Add more tickers as needed
]
START_DATE = "2024-12-23"  # Start date for data download
INTERVAL = "5m"  # Data interval

def fetch_and_append_data():
    """Fetch stock data and append it to the database."""
    conn = sqlite3.connect(DB_PATH)
    for stock in STOCK_LIST:
        table_name = stock.replace(".", "_")
        print(f"Processing stock: {stock}")

        # Ensure the table exists
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                datetime TEXT PRIMARY KEY,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                adj_close REAL,
                volume INTEGER
            )
        """)

        # Fetch the latest date in the database
        cursor = conn.cursor()
        cursor.execute(f"SELECT MAX(datetime) FROM {table_name}")
        last_date = cursor.fetchone()[0]

        # Determine the start date for fetching new data
        if last_date:
            start_date = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=5)
        else:
            start_date = datetime.strptime(START_DATE, "%Y-%m-%d")

        # Fetch data from Yahoo Finance
        data = yf.download(
            stock,
            start=start_date.strftime("%Y-%m-%d"),
            interval=INTERVAL,
            progress=False
        )

        if data.empty:
            print(f"No new data for {stock}.")
            continue

        # Prepare data for appending
        data.reset_index(inplace=True)
        data["Datetime"] = data["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
        data_to_append = data.rename(columns={
            "Datetime": "datetime",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume"
        })[["datetime", "open", "high", "low", "close", "adj_close", "volume"]]

        # Verify the data structure
        print(f"Data to append for {stock}:")
        print(data_to_append.head())

        # Append data to the table
        data_to_append.to_sql(table_name, conn, if_exists="append", index=False)
        print(f"Appended data for {stock}.")

    conn.close()


def push_database_to_github():
    """Commit and push the updated database to GitHub."""
    try:
        subprocess.run(["git", "add", DB_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "Update Nifty50 stocks database"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Database pushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error pushing database to GitHub: {e}")

if __name__ == "__main__":
    fetch_and_append_data()
    push_database_to_github()
