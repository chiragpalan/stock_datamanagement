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
    # Save the database to the correct directory
    db_path = os.path.join(os.getcwd(), "nifty50_data.db")  # Ensure it’s relative to the current working directory
    if not os.path.exists(db_path):
        open(db_path, 'w').close()  # Create database if it doesn’t exist
    return sqlite3.connect(db_path)

# Fetch data for all stocks
def fetch_and_store_stock_data():
    start_date = "2024-12-23"  # Fetch last 5 days of data
    print(start_date)
    end_date = datetime.now().strftime("%Y-%m-%d")

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
            print(data)
            print(symbol, data.columns)
            data.rename(columns = {"Adj Close":"adj_close"}, inplace = True)
            df['Datetime'] = df['Datetime'].dt.tz_localize(None)
            
            
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

    # return market_start <= now <= market_end and now.weekday() < 5  # Monday to Friday
    return True

if __name__ == "__main__":
    if is_market_open():
        fetch_and_store_stock_data()
