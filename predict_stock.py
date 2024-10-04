import yfinance as yf
import pandas as pd

# Download stock data
stock = yf.download('GOOG', start='2020-01-01', end='2023-01-01')

# Display the data
stock.to_csv('goog_stock.csv')
