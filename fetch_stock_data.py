import yfinance as yf
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os

# Define stock symbols for Nifty 50
def get_nifty50_symbols():
    # Replace this with the accurate list of Nifty 50 stocks
    return ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]  # Add the full list here

# Database connection
def get_db_connection():
    db_path = "nifty50_data.db"  # Local database file
    # Create database file if it does not exist
    if not os.path.exists(db_path):
        open(db_path, 'w').close()
    return sqlite3.connect(db_path)

# Fetch data for all stocks
def fetch_and_store_stock_data():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    start_date = (now - timedelta(days=5)).strftime('%Y-%m-%d')  # Fetch last 5 days of data
    end_date = now.strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    nifty50_symbols = get_nifty50_symbols()

    for symbol in nifty50_symbols:
        print(f"Fetching data for {symbol}")
        try:
            data = yf.download(
                symbol,
                start=start_date,
                end=end_date,
                interval="5m",
                progress=False
            )
            data.reset_index(inplace=True)
            data["Datetime"] = data["Datetime"].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')

            # Save to database
            table_name = symbol.replace(".", "_")
            data.to_sql(table_name, conn, if_exists='append', index=False)
            print(f"Data for {symbol} stored successfully.")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    conn.close()

# Scheduler logic
def is_market_open():
    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    market_start = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_end = now.replace(hour=15, minute=30, second=0, microsecond=0)

    return market_start <= now <= market_end and now.weekday() < 5  # Monday to Friday

if __name__ == "__main__":
    if is_market_open():
        fetch_and_store_stock_data()
