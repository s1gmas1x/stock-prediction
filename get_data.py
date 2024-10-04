import yfinance as yf

# Function to inspect the available data in the financial statements
def inspect_statements(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch income statement and balance sheet
    income_statement = stock.income_stmt
    balance_sheet = stock.balance_sheet
    cashflow = stock.cashflow
 
    # Print Income Statement and Balance Sheet
    print("Income Statement:")
    print(income_statement)
    
    print("\nBalance Sheet:")
    print(balance_sheet)

    print("\nCashflow:")
    print(cashflow)


# Main execution to inspect the data for one stock (e.g., Apple)
ticker = "AAPL"  # Replace this with any stock ticker
inspect_statements(ticker)