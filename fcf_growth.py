import yfinance as yf
import pandas as pd

# ANSI escape codes for coloring
RED = '\033[91m'   # Red color
GREEN = '\033[92m' # Green color
RESET = '\033[0m'  # Reset color

def get_fcf_growth_rate(ticker):
    stock = yf.Ticker(ticker)
    cashflow = stock.cashflow.T

    # Extract Free Cash Flow (FCF) for the past few years
    if 'Free Cash Flow' in cashflow.columns:
        fcf = cashflow['Free Cash Flow']
        fcf = fcf.astype(float)  # Ensure FCF is of type float
        fcf = fcf.dropna()  # Drop NaN values
        fcf = fcf[::-1]  # Reverse the Series for correct year comparisons
    else:
        raise ValueError(f"Missing data for {ticker}: 'Free Cash Flow'")

    # Calculate FCF growth rate year over year
    growth_rates = (fcf - fcf.shift(1)) / fcf.shift(1) * 100  # Convert to percentage
    growth_rates = growth_rates.round(1)  # Round the growth rates to 1 decimal point
    growth_rates = growth_rates.dropna()  # Drop NaN values

    # Calculate overall growth from the earliest to the latest year
    earliest_fcf = fcf.iloc[0]  # First year (earliest in reversed Series)
    latest_fcf = fcf.iloc[-1]   # Last year (latest in reversed Series)

    if earliest_fcf == 0:
        raise ValueError("Earliest Free Cash Flow is zero; cannot compute growth.")

    overall_growth = ((latest_fcf - earliest_fcf) / earliest_fcf) * 100  # Overall growth
    overall_growth = round(overall_growth, 1)  # Round to 1 decimal point

    return growth_rates, overall_growth

if __name__ == "__main__":
    ticker = 'AAPL'  # Example stock
    try:
        fcf_growth, overall_growth = get_fcf_growth_rate(ticker)
        print(f"Free Cash Flow Growth Rate for {ticker} (Year-over-Year Comparison):")
        for year in sorted(fcf_growth.keys(), reverse=True):  # Reverse the order here
            previous_year = year.replace(year=year.year - 1)  # Get the previous year for context
            
            # Color output based on growth rate
            growth_rate = fcf_growth[year]
            color = RED if growth_rate < 10 else GREEN
            print(f"{previous_year.date()} to {year.date()}: {color}{growth_rate}%{RESET}")  # Format output
        
    
 # Color overall growth output
        overall_color = RED if overall_growth < 10 else GREEN
        print(f"\nOverall Growth Rate (Earliest to Latest Year): {overall_color}{overall_growth}%{RESET}\n")
    
    except Exception as e:
        print(f"Failed to calculate Free Cash Flow Growth Rate: {e}\n")