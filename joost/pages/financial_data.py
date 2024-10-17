import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_financials(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.quarterly_financials.T

    metrics = {
        "Revenue": "Total Revenue",
        "COGS": "Cost Of Revenue",
        "EBIT": "Ebit",
        "Net Income": "Net Income",
        "R&D": "Research Development",
        "S&GA": "Selling General Administrative Expense"
    }

    filtered_data = {metric: financials.get(column, [f"Metric '{column}' not found"] * len(financials.index))
                     for metric, column in metrics.items()}

    if "Ebit" in financials.columns and "Depreciation" in stock.cashflow.columns:
        if len(financials["Ebit"]) == len(stock.cashflow.loc["Depreciation"]):
            filtered_data["EBITDA"] = financials["Ebit"] + stock.cashflow.loc["Depreciation"]
        else:
            filtered_data["EBITDA"] = [f"EBITDA calculation error (length mismatch)"] * len(financials.index)
    else:
        filtered_data["EBITDA"] = [f"EBITDA could not be calculated"] * len(financials.index)

    return pd.DataFrame(filtered_data)

def get_valuation_metrics(ticker):
    stock = yf.Ticker(ticker)
    return {"P/E Ratio": stock.info.get("forwardPE", None)}

def get_financials_for_multiple(tickers):
    ticker_list = [t.strip().upper() for t in tickers.split(',')]
    combined_financials, combined_valuations = {}, {}

    for ticker in ticker_list:
        try:
            combined_financials[ticker] = get_financials(ticker)
            combined_valuations[ticker] = get_valuation_metrics(ticker)
        except Exception as e:
            combined_financials[ticker] = f"Error fetching data: {e}"
            combined_valuations[ticker] = f"Error fetching data: {e}"

    return combined_financials, combined_valuations

# Plot financial data over time
def plot_financials(financials, ticker):
    plt.figure(figsize=(10, 6))
    for metric in ["Revenue", "EBITDA", "EBIT"]:
        if metric in financials.columns:
            plt.plot(financials.index, financials[metric], label=metric, marker="o")

    plt.title(f"Quarterly Financial Data for {ticker}")
    plt.xlabel("Quarter")
    plt.ylabel("Value (in billions)")
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)

# Main page for financial dashboard
def p_and_l_page():
    st.title("Quarterly Financial P&L and Valuation Dashboard")
    st.write("""
    Use this page to fetch key financial metrics (P&L) and valuation ratios for selected stocks using Yahoo Finance (yFinance).
    The following metrics will be extracted:
    - **P&L Metrics**: Revenue, COGS, EBITDA, EBIT, Net Income, R&D, S&GA
    - **Valuation Metrics**: P/E Ratio
    """)

    ticker_input = st.text_input("Enter stock ticker symbols (comma-separated, e.g., AAPL, MSFT):", "AAPL")

    if st.button("Get Data"):
        with st.spinner("Fetching data..."):
            financials, valuations = get_financials_for_multiple(ticker_input)
            st.session_state['financial_data'] = financials

            for ticker, data in financials.items():
                if isinstance(data, str):  # Handle error messages
                    st.error(f"{ticker}: {data}")
                else:
                    st.subheader(f"Quarterly Profit & Loss Statement for {ticker}")
                    st.dataframe(data.style.format(precision=2, na_rep='N/A').set_properties(
                        **{'background-color': 'lightcyan', 'color': 'black', 'border-color': 'gray', 'font-size': '14px'}
                    ))

                    st.subheader(f"Valuation Metrics for {ticker}")
                    valuation_df = pd.DataFrame(valuations[ticker], index=[ticker])
                    st.table(valuation_df)

                    if st.button(f"Visualize {ticker} Financials Over Time", key=f"visualize_{ticker}"):
                        st.session_state['selected_ticker'] = ticker
                        st.session_state['plot_data'] = data

    # Visualization section
    if 'plot_data' in st.session_state:
        st.subheader(f"Visualization for {st.session_state['selected_ticker']}")
        plot_financials(st.session_state['plot_data'], st.session_state['selected_ticker'])

# Run the application
p_and_l_page()
