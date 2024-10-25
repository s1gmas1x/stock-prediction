import yfinance as yf
import pandas as pd
from sales_growth import get_sales_growth_rate
from equity_growth import get_equity_growth_rate
from eps_growth import get_eps_growth_rate
from fcf_growth import get_fcf_growth_rate
from roic_calc import calculate_roic

# ANSI escape codes for coloring
RED = '\033[91m'   # Red color
GREEN = '\033[92m' # Green color
RESET = '\033[0m'  # Reset color

def display_metrics(ticker):
    try:
        # Sales Growth Rate
        sales_growth, overall_sales_growth = get_sales_growth_rate(ticker)
        print(f"\nSales Growth Rate for {ticker}:")
        for year in sorted(sales_growth.keys(), reverse=True):
            growth_rate = sales_growth[year]
            color = RED if growth_rate < 10 else GREEN
            print(f"{year}: {color}{growth_rate}%{RESET}")
        overall_color = RED if overall_sales_growth < 10 else GREEN
        print(f"Overall Sales Growth: {overall_color}{overall_sales_growth}%{RESET}")

        # Equity Growth Rate
        equity_growth, overall_equity_growth = get_equity_growth_rate(ticker)
        print(f"\nEquity Growth Rate for {ticker}:")
        for year in sorted(equity_growth.keys(), reverse=True):
            growth_rate = equity_growth[year]
            color = RED if growth_rate < 10 else GREEN
            print(f"{year}: {color}{growth_rate}%{RESET}")
        overall_color = RED if overall_equity_growth < 10 else GREEN
        print(f"Overall Equity Growth: {overall_color}{overall_equity_growth}%{RESET}")

        # EPS Growth Rate
        eps_growth, overall_eps_growth = get_eps_growth_rate(ticker)
        print(f"\nEPS Growth Rate for {ticker}:")
        for year in sorted(eps_growth.keys(), reverse=True):
            growth_rate = eps_growth[year]
            color = RED if growth_rate < 10 else GREEN
            print(f"{year}: {color}{growth_rate}%{RESET}")
        overall_color = RED if overall_eps_growth < 10 else GREEN
        print(f"Overall EPS Growth: {overall_color}{overall_eps_growth}%{RESET}")

        # Free Cash Flow Growth Rate
        fcf_growth, overall_fcf_growth = get_fcf_growth_rate(ticker)
        print(f"\nFree Cash Flow Growth Rate for {ticker}:")
        for year in sorted(fcf_growth.keys(), reverse=True):
            growth_rate = fcf_growth[year]
            color = RED if growth_rate < 10 else GREEN
            print(f"{year}: {color}{growth_rate}%{RESET}")
        overall_color = RED if overall_fcf_growth < 10 else GREEN
        print(f"Overall FCF Growth: {overall_color}{overall_fcf_growth}%{RESET}")

        # ROIC
        roic_results, overall_roic = calculate_roic(ticker)
        print(f"\nROIC for {ticker}:")
        for year, roic in roic_results.items():
            color = RED if roic < 10 else GREEN
            print(f"{year}: {color}{roic}%{RESET}")
        overall_color = RED if overall_roic < 10 else GREEN
        print(f"Overall ROIC: {overall_color}{overall_roic}%{RESET}")

    except Exception as e:
        print(f"Failed to calculate metrics for {ticker}: {e}\n")

if __name__ == "__main__":
    ticker = 'MSFT'  # Example stock
    display_metrics(ticker)