import streamlit as st
import yfinance as yf
import pandas as pd

def get_financials(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials.T
    return financials

def main():
    st.title("Financial P&L Dashboard")
    st.write("""
    This app fetches the financial Profit & Loss (P&L) statement for a selected stock using yFinance.
    """)


    ticker = st.text_input("Enter stock ticker symbol (e.g., AAPL, MSFT, TSLA)", "AAPL")

    if st.button("Get P&L Data"):
        try:
            # Fetch financials
            financial_data = get_financials(ticker)
            
            if financial_data.empty:
                st.write("No financial data found for the selected stock.")
            else:
                st.subheader(f"Profit & Loss Statement for {ticker.upper()}")
                # Display the data
                st.dataframe(financial_data)
        except Exception as e:
            st.error(f"Error fetching data: {e}")

