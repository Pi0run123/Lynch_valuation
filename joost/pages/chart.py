import plotly.express as px
import streamlit as st
import yfinance as yf
from datetime import date

# Theme handling
IS_DARK_THEME = True

st.title("Stock Chart")
st.write("Provide information to show the chart")

# User input for stock ticker, start date, and end date
assets = st.text_input("Ticker (e.g., AAPL) should be comma separated")
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
            data = yf.download(assets, start=date1, end=date2)

            if data.empty:
                st.error(f"No data found for ticker symbol {assets} within the given date range.")
            else:
                # Plotly Express line chart
                fig = px.line(data, x=data.index, y='Close', title=f'Closing Prices for {assets}')
                st.plotly_chart(fig)

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
