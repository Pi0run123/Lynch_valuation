# Description: This script contains the code to show a dialog box to insert stock information and show the stock price chart.
import plotly.express as px
import streamlit as st
import yfinance as yf


# def show_stock_selector():
st.write("Provide information to show the chart")

ticker = st.text_input("Ticker (e.g., AAPL)")
date1 = st.date_input("Start date")
date2 = st.date_input("End date")

if st.button("Submit"):
    if not ticker:
        st.error("Please enter a valid ticker symbol.")
    elif date1 >= date2:
        st.error("Start date must be before the end date.")
    else:
        try:
            st.write("Fetching data...")
            data = yf.download(ticker, start=date1, end=date2)
            
            if data.empty:
                st.error(f"No data found for ticker symbol {ticker} within the given date range.")
            else:
                fig = px.line(data, x=data.index, y='Close', title=f"{ticker} Stock Price")
                st.plotly_chart(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")

