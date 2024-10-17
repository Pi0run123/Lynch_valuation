import streamlit as st
import yfinance as yf
import pandas as pd

# Function to fetch financial data for a stock
def get_financials(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials.T
    return financials

# Function to fetch financials for multiple tickers
def get_financials_for_multiple(tickers):
    ticker_list = [t.strip().upper() for t in tickers.split(',')]
    combined_financials = {}

    for ticker in ticker_list:
        try:
            financial_data = get_financials(ticker)
            if not financial_data.empty:
                combined_financials[ticker] = financial_data
        except Exception as e:
            combined_financials[ticker] = f"Error fetching data: {e}"

    return combined_financials

# Page for fetching financial P&L statements
def p_and_l_page():
    st.title("Financial P&L Dashboard")
    st.write("""
    Use this page to fetch the financial Profit & Loss (P&L) statement for selected stocks using Yahoo Finance (yFinance).
    """)

    # Create a text input box for ticker symbols
    st.subheader("Input Ticker Symbols")
    ticker_input = st.text_input("Enter stock ticker symbols (comma-separated, e.g., AAPL, MSFT, TSLA):", "AAPL")

    # Create a button to trigger data fetching
    if st.button("Get P&L Data"):
        with st.spinner("Fetching data..."):
            # Fetch financial data for the entered tickers
            financials = get_financials_for_multiple(ticker_input)

            # Loop through the fetched financials and display each stock's data
            for ticker, data in financials.items():
                if isinstance(data, str):  # If there is an error message
                    st.error(f"{ticker}: {data}")
                else:
                    st.subheader(f"Profit & Loss Statement for {ticker}")
                    # Display the financial data in a styled table
                    st.dataframe(data.style.format(precision=2, na_rep='N/A').set_properties(**{
                        'background-color': 'lightcyan',
                        'color': 'black',
                        'border-color': 'gray',
                        'font-size': '14px'
                    }))
                    st.write("\n")  # Add space between tickers' data

# Run the page function
p_and_l_page()
