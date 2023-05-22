import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq

# Set up pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Define the search term and time range
search_term = input("Enter the keyword you want to search on Google Trends: ")  # Replace with the desired search term
start_date = "2020-10-01"  # Replace with the start date
end_date = "2020-11-30"  # Replace with the end date

# Get Google Trends data
pytrends.build_payload([search_term], timeframe=f"{start_date} {end_date}")
search_data = pytrends.interest_over_time()

# Reset index and rename columns
search_data.reset_index(inplace=True)
search_data.rename(columns={"date": "Day", search_term: "Search Frequency"}, inplace=True)

# Convert "Day" column to datetime format
search_data["Day"] = pd.to_datetime(search_data["Day"])

# Fetch stock data using yfinance
stock_symbol = "AMZN"  # Replace with the desired stock symbol
stock_data = yf.download(stock_symbol, start=start_date, end=end_date, progress=False)

# Reset index of stock data and rename index column to "Day"
stock_data.reset_index(inplace=True)
stock_data.rename(columns={"Date": "Day"}, inplace=True)

# Merge search data and stock data based on the "Day" column
merged_data = pd.merge(search_data, stock_data, on="Day")

# Display daily stock prices and search frequency
daily_stock_prices = merged_data[["Day", "Close"]]
daily_search_frequency = merged_data[["Day", "Search Frequency"]]
correlation = daily_stock_prices["Close"].corr(daily_search_frequency["Search Frequency"])

print("Daily Stock Prices:")
print(daily_stock_prices)
print()
print("Daily Search Frequency:")
print(daily_search_frequency)
print()
print("Correlation:")
print(correlation)
