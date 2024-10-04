import yfinance as yf

def calculate_roic(ticker):
    # Fetch stock data
    stock = yf.Ticker(ticker)

    # Fetch the income statement and balance sheet, transposed for easier access
    income_statement = stock.income_stmt.T
    balance_sheet = stock.balance_sheet.T

    # Prepare a dictionary to store ROIC results by year
    roic_results = {}

    # Get the number of years to consider (up to 5 years of data)
    years = income_statement.index[:5]  # Adjust as needed

    for i, year in enumerate(years):
        try:
            # Extract relevant data using iloc
            ebit = income_statement.iloc[i]['EBIT']
            tax_rate = income_statement.iloc[i]['Tax Rate For Calcs']
            total_debt = balance_sheet.iloc[i]['Total Debt']
            cash_equivalents = balance_sheet.iloc[i]['Cash And Cash Equivalents']

            # Calculate total equity (use stockholder equity if available, otherwise calculate it)
            if 'Total Stockholder Equity' in balance_sheet.columns:
                total_equity = balance_sheet['Total Stockholder Equity'].iloc[i]
            else:
                total_assets = balance_sheet.iloc[i]['Total Assets']
                total_liabilities = balance_sheet.iloc[i]['Total Liabilities Net Minority Interest']
                total_equity = total_assets - total_liabilities  # Calculate equity as assets - liabilities

            # Calculate invested capital
            invested_capital = total_debt + total_equity - cash_equivalents

            # Calculate ROIC
            roic = (ebit * (1 - tax_rate)) / invested_capital
            roic_results[year] = roic * 100  # Convert to percentage

        except IndexError as e:
            print(f"Missing data for {ticker} in year {year}: {e}")
        except Exception as e:
            print(f"Error calculating ROIC for {ticker} in year {year}: {e}")

    return roic_results

# Example usage
ticker = "AAPL"
roic_aapl = calculate_roic(ticker)

# Display the results in a formatted way
print(f"ROIC for {ticker} over the years:")
for year, roic in roic_aapl.items():
    print(f"{year}: {roic:.2f}%")
