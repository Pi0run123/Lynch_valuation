import plotly.express as px
import streamlit as st
import yfinance as yf
from datetime import date

# Theme handling
IS_DARK_THEME = True

st.title("Stock Chart")
st.write("Provide information to show the chart")

# User input for stock ticker, start date, and end date
assets = st.text_input("Ticker (e.g., AAPL, MSFT) should be comma separated")
date1 = st.date_input("Start date", value=date(2022, 1, 1))
date2 = st.date_input("End date", value=date.today())

if st.button("Submit"):
    if not assets:
        st.error("Please enter a valid ticker symbol.")
    elif date1 >= date2:
        st.error("Start date must be before the end date.")
    else:
        try:
            st.write("Fetching data...")
            tickers = [ticker.strip() for ticker in assets.split(',')]
            data = yf.download(tickers, start=date1, end=date2)

            if data.empty:
                st.error(f"No data found for ticker symbols {assets} within the given date range.")
            else:
                # If multiple stocks, the 'Close' prices will have multiple columns (one for each ticker)
                close_data = data['Close']
                close_data = close_data.reset_index().melt(id_vars='Date', var_name='Ticker', value_name='Close')

                # Plotly Express line chart
                fig = px.line(close_data, x='Date', y='Close', color='Ticker', title=f'Closing Prices for {assets}')
                st.plotly_chart(fig)

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
