import yfinance as yf
import pandas as pd

# Download stock data
stock = yf.download('AAPL', start='2020-01-01', end='2023-01-01')

# Display the data
print(stock.head())
