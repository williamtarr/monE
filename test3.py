import pandas as pd
import yfinance as yf

# Read the existing CSV file
csv_file_path = "aaplOctNov2020.csv"  # Replace with the actual file path of your CSV file
search_data = pd.read_csv(csv_file_path, skiprows=3, names=["Day", "aapl: (Canada)"])

# Convert "Day" column to datetime format
search_data["Day"] = pd.to_datetime(search_data["Day"], format="%Y-%m-%d")

# Fetch stock data using yfinance
stock_symbol = "AAPL"  # Replace with the desired stock symbol
stock_data = yf.download(stock_symbol, start=search_data["Day"].min(), end=search_data["Day"].max(), progress=False)

# Reset index of stock data and rename index column to "Day"
stock_data.reset_index(inplace=True)
stock_data.rename(columns={"Date": "Day"}, inplace=True)

# Merge search data and stock data based on the "Day" column
merged_data = pd.merge(search_data, stock_data, on="Day")

# Display daily stock prices and search frequency
daily_stock_prices = merged_data[["Day", "Close"]]
daily_search_frequency = merged_data[["Day", "aapl: (Canada)"]]
correlation = daily_stock_prices["Close"].corr(daily_search_frequency["aapl: (Canada)"])

print("Daily Stock Prices:")
print(daily_stock_prices)
print()
print("Daily Search Frequency:")
print(daily_search_frequency)
print()
print("Correlation:")
print(correlation)