import yfinance as yf
import os

# Directory to save CSV files
output_dir = "temp_csvs"

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
print(f"Directory '{output_dir}' created or already exists.")

# List of tickers
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

# Download data and save to CSV
for ticker in tickers:
    print(f"Downloading data for {ticker}...")
    stock_data = yf.download(ticker, period="1d", interval="5m")
    
    # Check if data is available
    if not stock_data.empty:
        file_name = ticker.replace(".", "_") + ".csv"
        file_path = os.path.join(output_dir, file_name)
        stock_data.to_csv(file_path)
        print(f"Data for {ticker} saved to {file_path}")
    else:
        print(f"No data available for {ticker}.")
