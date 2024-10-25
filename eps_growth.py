import yfinance as yf
import pandas as pd

# ANSI escape codes for coloring
RED = '\033[91m'   # Red color
GREEN = '\033[92m' # Green color
RESET = '\033[0m'  # Reset color

def get_eps_growth_rate(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials.T  # Fetch financials data

    # Extract EPS data for the past few years
    if 'Diluted EPS' in financials.columns:
        eps = financials['Diluted EPS']
        eps = eps.astype(float)  # Ensure EPS is of type float
        eps = eps.dropna()  # Drop NaN values
        eps = eps[::-1]  # Reverse the Series for correct year comparisons
    else:
        raise ValueError(f"Missing data for {ticker}: 'Earnings Per Share'")

    # Calculate EPS growth rate year over year
    growth_rates = (eps - eps.shift(1)) / eps.shift(1) * 100  # Convert to percentage
    growth_rates = growth_rates.round(1)  # Round the growth rates to 1 decimal point
    growth_rates = growth_rates.dropna()  # Drop NaN values

    # Calculate overall growth from the earliest to the latest year
    earliest_eps = eps.iloc[0]  # First year (earliest in reversed Series)
    latest_eps = eps.iloc[-1]   # Last year (latest in reversed Series)

    if earliest_eps == 0:
        raise ValueError("Earliest EPS is zero; cannot compute growth.")

    overall_growth = ((latest_eps - earliest_eps) / earliest_eps) * 100  # Overall growth
    overall_growth = round(overall_growth, 1)  # Round to 1 decimal point

    return growth_rates, overall_growth

if __name__ == "__main__":
    ticker = 'MSFT'  # Example stock
    try:
        eps_growth, overall_growth = get_eps_growth_rate(ticker)
        print(f"EPS (Diluted) Growth Rate for {ticker} (Year-over-Year Comparison):")
        for year in sorted(eps_growth.keys(), reverse=True):  # Reverse the order here
            previous_year = year.replace(year=year.year - 1)  # Get the previous year for context
            
            # Color output based on growth rate
            growth_rate = eps_growth[year]
            color = RED if growth_rate < 10 else GREEN
            print(f"{previous_year.date()} to {year.date()}: {color}{growth_rate}%{RESET}")  # Format output
        
        # Color overall growth output
        overall_color = RED if overall_growth < 10 else GREEN
        print(f"\nOverall Growth Rate (Earliest to Latest Year): {overall_color}{overall_growth}%{RESET}\n")
    
    except Exception as e:
        print(f"Failed to calculate EPS Growth Rate: {e}\n")