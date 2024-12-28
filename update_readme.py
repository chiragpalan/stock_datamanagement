import sqlite3
import pandas as pd
import os

# Path to the database
db_path = "nifty50_data.db"  # Adjust if necessary
conn = sqlite3.connect(db_path)

# Fetch all table names
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = [row[0] for row in conn.execute(query).fetchall()]

# Start Markdown content
markdown_content = "# Last 5 Rows of Each Table in `nifty50_data.db`\n\n"

# Process each table
for table in tables:
    markdown_content += f"## Table: {table}\n\n"
    try:
        # Fetch last 5 rows
        query = f"SELECT * FROM {table} ORDER BY ROWID DESC LIMIT 5;"
        df = pd.read_sql_query(query, conn)
        
        # Convert DataFrame to Markdown format
        markdown_content += df.to_markdown(index=False) + "\n\n"
    except Exception as e:
        markdown_content += f"Error reading table `{table}`: {e}\n\n"

# Close database connection
conn.close()

# Write to README.md
with open("README.md", "w") as f:
    f.write(markdown_content)

print("README.md updated successfully!")
