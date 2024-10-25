import yfinance as yf
import pandas as pd

# ANSI escape codes for coloring
RED = '\033[91m'   # Red color
GREEN = '\033[92m' # Green color
RESET = '\033[0m'  # Reset color

def get_equity_growth_rate(ticker):
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet.T  # Fetch balance sheet data

    # Check for a valid equity column name
    equity_column_name = None
    for column in balance_sheet.columns:
        if 'equity' in column.lower():  # Check if the column name contains 'equity'
            equity_column_name = column
            break

    if equity_column_name:
        equity = balance_sheet[equity_column_name]
        equity = equity.astype(float)  # Ensure equity is of type float
        equity = equity.dropna()  # Drop NaN values
        equity = equity[::-1]  # Reverse the Series for correct year comparisons
    else:
        raise ValueError(f"Missing data for {ticker}: 'Total Stockholder Equity'")

    # Calculate equity growth rate year over year
    growth_rates = (equity - equity.shift(1)) / equity.shift(1) * 100  # Convert to percentage
    growth_rates = growth_rates.round(1)  # Round the growth rates to 1 decimal point
    growth_rates = growth_rates.dropna()  # Drop NaN values

    # Calculate overall growth from the earliest to the latest year
    earliest_equity = equity.iloc[0]  # First year (earliest in reversed Series)
    latest_equity = equity.iloc[-1]   # Last year (latest in reversed Series)

    if earliest_equity == 0:
        raise ValueError("Earliest equity is zero; cannot compute growth.")

    overall_growth = ((latest_equity - earliest_equity) / earliest_equity) * 100  # Overall growth
    overall_growth = round(overall_growth, 1)  # Round to 1 decimal point

    return growth_rates, overall_growth

if __name__ == "__main__":
    ticker = 'AAPL'  # Example stock
    try:
        equity_growth, overall_growth = get_equity_growth_rate(ticker)
        print(f"Equity Growth Rate for {ticker} (Year-over-Year Comparison):")
        for year in sorted(equity_growth.keys(), reverse=True):  # Reverse the order here
            previous_year = year.replace(year=year.year - 1)  # Get the previous year for context
            
            # Color output based on growth rate
            growth_rate = equity_growth[year]
            color = RED if growth_rate < 10 else GREEN
            print(f"{previous_year.date()} to {year.date()}: {color}{growth_rate}%{RESET}")  # Format output
        
        # Color overall growth output
        overall_color = RED if overall_growth < 10 else GREEN
        print(f"\nOverall Growth Rate (Earliest to Latest Year): {overall_color}{overall_growth}%{RESET}\n")
    
    except Exception as e:
        print(f"Failed to calculate Equity Growth Rate: {e}\n")