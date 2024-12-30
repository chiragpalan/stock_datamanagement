import yfinance as yf
import os

# Create the directory if it doesn't exist
# os.makedirs("temp_csvs", exist_ok=True)

# List of tickers
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

# Loop through each ticker, download the data, and save it to a CSV file
for ticker in tickers:
    # Download data for the ticker
    stock_data = yf.download(ticker, period="1d", interval="5m")
    
    # Check if data is available
    if not stock_data.empty:
        # Format the ticker for the file name
        file_name = ticker.replace(".", "_")
        print(stock_data)
        
        # Save the data to a CSV file in the temp_csvs folder
        stock_data.to_csv(f"temp_csvs/{file_name}.csv")
        print(f"Data for {ticker} saved to {file_name}.csv")
    else:
        print(f"No data available for {ticker}")
