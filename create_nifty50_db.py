import sqlite3
import os

def get_db_connection():
    db_path = "nifty50_data.db"  # Local database file
    # Create database file if it does not exist
    if not os.path.exists(db_path):
        open(db_path, 'w').close()
    return sqlite3.connect(db_path)

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Replace this with the accurate list of Nifty 50 stocks
    nifty50_symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

    for symbol in nifty50_symbols:
        table_name = symbol.replace(".", "_")
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            Datetime TEXT PRIMARY KEY,
            Open REAL,
            High REAL,
            Low REAL,
            Close REAL,
            Adj_Close REAL,
            Volume INTEGER
        );
        """
        cursor.execute(create_table_query)
        print(f"Table for {symbol} created or already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables setup completed.")
