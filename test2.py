import pandas as pd
import yfinance as yf
from datetime import datetime

# Read the existing CSV file
csv_file_path = "aaplOctQuarterly.csv"  # Replace with the actual file path of your CSV file
search_data = pd.read_csv(csv_file_path, skiprows=3, names=["Day", "aapl: (Canada)"])

# Convert "Day" column to datetime format
search_data["Day"] = pd.to_datetime(search_data["Day"], format="%Y-%m-%d")

# Extract the desired time range
start_date = datetime(2020, 10, 28)
end_date = datetime(2020, 10, 30)
search_data_range = search_data[(search_data["Day"] >= start_date) & (search_data["Day"] <= end_date)]

# Fetch stock data using yfinance
stock_symbol = "AAPL"  # Replace with the desired stock symbol
stock_data = yf.download(stock_symbol, start=start_date, end=end_date, progress=False)

# Merge the search data and stock data on date
merged_data = pd.merge(search_data_range, stock_data, left_on="Day", right_on=stock_data.index)

# Calculate the correlation between search data and stock prices
correlation = merged_data["aapl: (Canada)"].corr(merged_data["Close"])

# Print the correlation value
print(f"Correlation between search term 'AAPL' and stock prices: {correlation}")
