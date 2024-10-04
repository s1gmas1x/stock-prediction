import yfinance as yf

# Function to calculate ROIC for a stock
def calculate_roic(ticker):
    stock = yf.Ticker(ticker)
    
    try:
        # Fetch financial statements
        income_statement = stock.income_stmt
        balance_sheet = stock.balance_sheet

        # Extract relevant data using .iloc for future compatibility
        ebit = income_statement.loc['EBIT'].iloc[0]  # Most recent year EBIT
        tax_rate = income_statement.loc['Tax Rate For Calcs'].iloc[0]  # Use tax rate for calcs

        # Try to get Total Stockholder Equity, otherwise compute it
        if 'Total Stockholder Equity' in balance_sheet.index:
            total_equity = balance_sheet.loc['Total Stockholder Equity'].iloc[0]
        else:
            total_assets = balance_sheet.loc['Total Assets'].iloc[0]  # Total assets
            total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]  # Total liabilities
            total_equity = total_assets - total_liabilities  # Calculate equity as assets - liabilities

        total_debt = balance_sheet.loc['Total Debt'].iloc[0]  # Total debt

        # Calculate NOPAT (Net Operating Profit After Tax)
        nopat = ebit * (1 - tax_rate)

        # Calculate invested capital (equity + debt)
        invested_capital = total_equity + total_debt

        # Calculate ROIC
        roic = nopat / invested_capital if invested_capital != 0 else None

        if roic is not None:
            print(f"ROIC for {ticker}: {roic:.2%}")
        else:
            print(f"Failed to calculate ROIC for {ticker}: Invested Capital is zero")
    
    except KeyError as e:
        print(f"Missing data for {ticker}: {e}")
        print(f"Failed to calculate ROIC for {ticker}")

# Main execution to calculate ROIC for one stock (e.g., Apple)
ticker = "AAPL"  # Replace this with any stock ticker
calculate_roic(ticker)