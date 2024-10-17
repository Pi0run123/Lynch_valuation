import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Format numbers with thousand separators
def format_number(num):
    return f"{num:,.0f}".replace(',', '.').replace('.', ',', 1)

# Main page for financial dashboard
st.title("Quarterly Financial P&L and Valuation Dashboard")
st.write("""
Use this page to fetch key financial metrics (P&L) and valuation ratios for selected stocks using Yahoo Finance (yFinance).
The following metrics will be extracted:
- **P&L Metrics**: Revenue, COGS, Net Income
- **Valuation Metrics**: P/E Ratio
""")

ticker_input = st.text_input("Enter stock ticker symbols (comma-separated, e.g., AAPL, MSFT):", "AAPL")

# Fetch the data when the button is clicked
if st.button("Get Data"):
    tickers = [t.strip().upper() for t in ticker_input.split(',')]
    combined_financials = {}
    combined_valuations = {}

    # Loop through each ticker and fetch financials and valuations
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            financials = stock.quarterly_financials.T
            
            # Collect specified financial metrics
            filtered_data = pd.DataFrame({
                "Revenue": financials.get("Total Revenue", [f"Metric not found"] * len(financials.index)),
                "COGS": financials.get("Cost Of Revenue", [f"Metric not found"] * len(financials.index)),
                "Net Income": financials.get("Net Income", [f"Metric not found"] * len(financials.index))
            })

            combined_financials[ticker] = filtered_data

            # Get the valuation metric
            pe_ratio = stock.info.get("forwardPE", None)
            combined_valuations[ticker] = {"P/E Ratio": pe_ratio}

        except Exception as e:
            combined_financials[ticker] = f"Error fetching data: {e}"
            combined_valuations[ticker] = f"Error fetching data: {e}"

    # Save the data into session state to persist after button clicks
    st.session_state['financial_data'] = combined_financials
    st.session_state['valuation_data'] = combined_valuations

# Display the financial data if it's available
if 'financial_data' in st.session_state:
    financials = st.session_state['financial_data']
    valuations = st.session_state['valuation_data']

    for ticker, data in financials.items():
        if isinstance(data, str):
            st.error(f"{ticker}: {data}")
        else:
            st.subheader(f"Quarterly Profit & Loss Statement for {ticker}")
            
            # Format the data for better display
            formatted_data = data.applymap(lambda x: format_number(x) if isinstance(x, (int, float)) else x)
            st.dataframe(formatted_data.style.set_properties(
                {'background-color': 'lightcyan', 'color': 'black', 'border-color': 'gray', 'font-size': '14px'}
            ))

            st.subheader(f"Valuation Metrics for {ticker}")
            valuation_df = pd.DataFrame(valuations[ticker], index=[ticker])
            valuation_df = valuation_df.applymap(lambda x: format_number(x) if isinstance(x, (int, float)) else x)
            st.table(valuation_df)

            # Visualize financials for each ticker
            if st.button(f"Visualize {ticker} Financials Over Time", key=f"visualize_{ticker}"):
                st.session_state['selected_ticker'] = ticker
                st.session_state['plot_data'] = data

# Display the plot if the data exists in session state
if 'plot_data' in st.session_state:
    selected_ticker = st.session_state['selected_ticker']
    plot_data = st.session_state['plot_data'].reset_index()

    st.subheader(f"Visualization for {selected_ticker}")

    # Plot the data using Plotly
    fig = px.line(plot_data, x='index', y=['Revenue', 'COGS', 'Net Income'], markers=True,
                  labels={'index': 'Quarter', 'value': 'Value (in billions)', 'variable': 'Metrics'},
                  title=f"Quarterly Financial Data for {selected_ticker}")

    fig.update_layout(xaxis_tickangle=-45)  # Rotate x-axis labels
    st.plotly_chart(fig)
