import yfinance as yf
import pandas as pd

def get_sales_growth_rate(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials.T

    # Extract Total Revenue (Sales) for the past few years
    if 'Total Revenue' in financials.columns:
        revenues = financials['Total Revenue']
        revenues = revenues.astype(float)  # Ensure revenues are of type float
        revenues = revenues[::-1]  # Reverse the Series for correct year comparisons
    else:
        raise ValueError(f"Missing data for {ticker}: 'Total Revenue'")

    # Calculate sales growth rate year over year
    growth_rates = (revenues - revenues.shift(1)) / revenues.shift(1) * 100  # Convert to percentage
    growth_rates = growth_rates.round(1)  # Round the growth rates to 1 decimal point
    growth_rates = growth_rates.dropna()  # Drop NaN values

    return growth_rates

if __name__ == "__main__":
    ticker = 'INTC'  # Example stock
    try:
        sales_growth = get_sales_growth_rate(ticker)
        print(f"Sales Growth Rate for {ticker} (Year-over-Year Comparison):")
        for year in sorted(sales_growth.keys(), reverse=True):  # Reverse the order here
            previous_year = year.replace(year=year.year - 1)  # Get the previous year for context
            print(f"{previous_year.date()} to {year.date()}: {sales_growth[year]}%")  # Format output
    except Exception as e:
        print(f"Failed to calculate Sales Growth Rate: {e}")