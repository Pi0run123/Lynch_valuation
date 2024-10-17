import plotly.express as px
import streamlit as st
import yfinance as yf
from datetime import date

# Theme handling
IS_DARK_THEME = True

st.title("Stock Analysis: Cumulative Returns and Volatility")
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
                # -----------------------------
                # Cumulative Percentage Change
                # -----------------------------
                st.write("### Cumulative Percentage Change")

                close_data = data['Close'].pct_change()  # Daily percentage change
                cumulative_data = (1 + close_data).cumprod() - 1  # Cumulative return
                cumulative_data = cumulative_data * 100
                cumulative_data = cumulative_data.reset_index().melt(id_vars='Date', var_name='Ticker', value_name='Cumulative Percentage Change')
                fig_cumulative = px.line(cumulative_data, x='Date', y='Cumulative Percentage Change', color='Ticker', 
                                         title=f'Cumulative Percentage Change for {assets}')
                st.plotly_chart(fig_cumulative)

                # -----------------------------
                # Standard Deviation (Volatility).
                # -----------------------------
                st.write("### Volatility (Rolling Standard Deviation)")

                rolling_std_data = data['Close'].rolling(window=20).std()

                rolling_std_data = rolling_std_data.reset_index().melt(id_vars='Date', var_name='Ticker', value_name='Standard Deviation')

                fig_std_dev = px.line(rolling_std_data, x='Date', y='Standard Deviation', color='Ticker', 
                                      title=f'Rolling 20-Day Standard Deviation for {assets} (Volatility)')
                st.plotly_chart(fig_std_dev)

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
