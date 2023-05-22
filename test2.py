import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq

# Set up pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# Function to get Google Trends data for a specific search term
def get_search_data(search_term, start_date, end_date):
    pytrends.build_payload([search_term], timeframe=f"{start_date} {end_date}")
    search_data = pytrends.interest_over_time()
    search_data.reset_index(inplace=True)
    search_data.rename(columns={"date": "Day", search_term: "Search Frequency"}, inplace=True)
    search_data["Day"] = pd.to_datetime(search_data["Day"])
    return search_data

# Function to calculate correlation between search frequency and stock prices
def calculate_correlation(stock_data, search_data):
    merged_data = pd.merge(search_data, stock_data, on="Day")
    daily_stock_prices = merged_data[["Day", "Close"]]
    daily_search_frequency = merged_data[["Day", "Search Frequency"]]
    correlation = daily_stock_prices["Close"].corr(daily_search_frequency["Search Frequency"])
    return correlation

# Function to fetch stock data using yfinance
def get_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date, progress=False)
    stock_data.reset_index(inplace=True)
    stock_data.rename(columns={"Date": "Day"}, inplace=True)
    return stock_data

# Main function
def main():
    # User input for stock symbol
    stock_symbol = input("Enter the stock symbol: ")
    
    # User input for time range
    #start_date = input("Enter the start date (YYYY-MM-DD): ")
    #end_date = input("Enter the end date (YYYY-MM-DD): ")
    start_date = "2020-10-01"  # Replace with the start date
    end_date = "2020-10-10"  # Replace with the end date
    
    # Fetch stock data
    stock_data = get_stock_data(stock_symbol, start_date, end_date)
    
    # Fetch the top 10 stock-related search terms
    pytrends.build_payload([stock_symbol], timeframe=f"{start_date} {end_date}")
    related_queries = pytrends.related_queries()
    top_search_terms = related_queries[stock_symbol]['top']['query'].tolist()[:10]
    
    # Calculate correlation for each search term
    correlations = []
    for search_term in top_search_terms:
        search_data = get_search_data(search_term, start_date, end_date)
        correlation = calculate_correlation(stock_data, search_data)
        correlations.append((search_term, correlation))
    
    # Sort correlations in descending order
    correlations.sort(key=lambda x: x[1], reverse=True)
    
    # Print correlations
    print("Correlations:")
    for term, correlation in correlations:
        print(f"{term}: {correlation}")

# Run the main function
if __name__ == "__main__":
    main()
