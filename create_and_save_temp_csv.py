import yfinance as yf
import os
from datetime import datetime, timedelta

# Define the output directory
output_dir = "temp_csvs"
os.makedirs(output_dir, exist_ok=True)

# List of tickers
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

# Download and save data for each ticker
for ticker in tickers:
    stock_data = yf.download(ticker, period="1d", interval="5m")
    
    if not stock_data.empty:
        # Format the ticker name for the file
        file_name = ticker.replace(".", "_")
        file_path = os.path.join(output_dir, f"{file_name}.csv")
        stock_data.rename(columns = {"Adj Close":"Adj_Close"}, inplace = True)
        print(stock_data)
        stock_data['Datetime'] = stock_data['Datetime'].dt.tz_localize(None)
        print(stock_data)
        # Save to CSV
        stock_data.to_csv(file_path,index=True, mode='w')
        print(f"Saved data for {ticker} to {file_path}")
    else:
        print(f"No data found for {ticker}")
