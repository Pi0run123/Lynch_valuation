import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch financial data for a stock (Quarterly)
def get_financials(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.quarterly_financials.T

    # Filter for specific P&L metrics
    metrics = {
        "Revenue": "Total Revenue",
        "COGS": "Cost Of Revenue",  # Could be "Cost of Goods Sold"
        "EBIT": "Ebit",            # Earnings Before Interest and Taxes
        "Net Income": "Net Income",
        "R&D": "Research Development",
        "S&GA": "Selling General Administrative Expense"
    }

    filtered_data = pd.DataFrame()

    for metric, column in metrics.items():
        if column in financials.columns:
            filtered_data[metric] = financials[column]
        else:
            filtered_data[metric] = [f"Metric '{column}' not found"] * len(financials.index)

    # Calculate EBITDA if possible
    if "Ebit" in financials.columns and "Depreciation" in stock.cashflow.columns:
        # Ensure both have the same index length before adding them
        if len(financials["Ebit"]) == len(stock.cashflow.loc["Depreciation"]):
            ebitda = financials["Ebit"] + stock.cashflow.loc["Depreciation"]
            filtered_data["EBITDA"] = ebitda
        else:
            filtered_data["EBITDA"] = [f"EBITDA could not be calculated (length mismatch)"] * len(financials.index)
    else:
        filtered_data["EBITDA"] = [f"EBITDA could not be calculated"] * len(financials.index)

    return filtered_data

# Function to calculate P/E Ratio
def get_valuation_metrics(ticker):
    stock = yf.Ticker(ticker)
    pe_ratio = stock.info.get("forwardPE", None)

    return {
        "P/E Ratio": pe_ratio
    }

# Function to fetch financials for multiple tickers (Quarterly)
def get_financials_for_multiple(tickers):
    ticker_list = [t.strip().upper() for t in tickers.split(',')]
    combined_financials = {}
    combined_valuations = {}

    for ticker in ticker_list:
        try:
            financial_data = get_financials(ticker)
            valuation_data = get_valuation_metrics(ticker)

            if not financial_data.empty:
                combined_financials[ticker] = financial_data
                combined_valuations[ticker] = valuation_data
        except Exception as e:
            combined_financials[ticker] = f"Error fetching data: {e}"
            combined_valuations[ticker] = f"Error fetching data: {e}"

    return combined_financials, combined_valuations

# Function to visualize financial data over time
def plot_financials(financials, ticker):
    plt.figure(figsize=(10, 6))

    if "Revenue" in financials.columns:
        plt.plot(financials.index, financials["Revenue"], label="Revenue", marker="o")
    if "EBITDA" in financials.columns:
        plt.plot(financials.index, financials["EBITDA"], label="EBITDA", marker="o")
    if "EBIT" in financials.columns:
        plt.plot(financials.index, financials["EBIT"], label="EBIT", marker="o")

    plt.title(f"Quarterly Financial Data for {ticker}")
    plt.xlabel("Quarter")
    plt.ylabel("Value (in billions)")
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)

# Page for fetching financial P&L statements and valuation metrics
def p_and_l_page():
    st.title("Quarterly Financial P&L and Valuation Dashboard")
    st.write("""
    Use this page to fetch key financial metrics (P&L) and valuation ratios for selected stocks using Yahoo Finance (yFinance).
    The following metrics will be extracted:
    - **P&L Metrics**: Revenue, COGS, EBITDA, EBIT, Net Income, R&D, S&GA
    - **Valuation Metrics**: P/E Ratio
    """)

    # Create a text input box for ticker symbols
    st.subheader("Input Ticker Symbols")
    ticker_input = st.text_input("Enter stock ticker symbols (comma-separated, e.g., AAPL, MSFT, TSLA):", "AAPL")

    # Button to fetch data
    if st.button("Get Data"):
        with st.spinner("Fetching data..."):
            # Fetch financial and valuation data for the entered tickers
            financials, valuations = get_financials_for_multiple(ticker_input)

            # Store data in session state for visualization later
            st.session_state['financial_data'] = financials

            # Display financial data for each stock
            for ticker, data in financials.items():
                if isinstance(data, str):  # If there is an error message
                    st.error(f"{ticker}: {data}")
                else:
                    st.subheader(f"Quarterly Profit & Loss Statement for {ticker}")
                    # Display the financial data in a styled table
                    st.dataframe(data.style.format(precision=2, na_rep='N/A').set_properties(**{
                        'background-color': 'lightcyan',
                        'color': 'black',
                        'border-color': 'gray',
                        'font-size': '14px'
                    }))
                    st.write("\n")

                    # Show valuation metrics in a separate table
                    st.subheader(f"Valuation Metrics for {ticker}")
                    valuation_df = pd.DataFrame(valuations[ticker], index=[ticker])
                    st.table(valuation_df)

                    # Button for visualization
                    if st.button(f"Visualize {ticker} Financials Over Time", key=f"visualize_{ticker}"):
                        st.session_state['selected_ticker'] = ticker

    # Check if data is available for visualization
    if 'financial_data' in st.session_state and 'selected_ticker' in st.session_state:
        ticker = st.session_state['selected_ticker']
        financial_data = st.session_state['financial_data'][ticker]
        st.subheader(f"Visualization for {ticker}")
        plot_financials(financial_data, ticker)

# Run the page function
p_and_l_page()
