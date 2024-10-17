import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_financials(ticker):
    stock = yf.Ticker(ticker)
    financials = stock.financials.T

    metrics = {
        "Revenue": "Total Revenue",
        "COGS": "Cost Of Revenue",  
        "EBIT": "Ebit",           
        "Net Income": "Net Income",
        "R&D": "Research Development",
        "S&GA": "Selling General Administrative Expense"
    }

    filtered_data = pd.DataFrame()

    for metric, column in metrics.items():
        if column in financials.columns:
            filtered_data[metric] = financials[column]
        else:
            filtered_data[metric] = [f"Metric '{column}' not found"]

    # Calculate EBITDA if possible
    if "Ebit" in financials.columns and "Depreciation" in stock.cashflow.columns:
        ebitda = financials["Ebit"] + stock.cashflow.loc["Depreciation"]
        filtered_data["EBITDA"] = ebitda
    else:
        filtered_data["EBITDA"] = [f"EBITDA could not be calculated"]

    if "Total Revenue" in financials.columns:
        filtered_data["Revenue Growth (%)"] = financials["Total Revenue"].pct_change() * 100
    else:
        filtered_data["Revenue Growth (%)"] = "N/A"

    return filtered_data

def get_valuation_metrics(ticker):
    stock = yf.Ticker(ticker)
    ev = stock.info.get("enterpriseValue", None)
    pe_ratio = stock.info.get("forwardPE", None)

    financials = stock.financials.T

    if "Ebit" in financials.columns and "Depreciation" in stock.cashflow.columns:
        ebitda = financials["Ebit"] + stock.cashflow.loc["Depreciation"]
    else:
        ebitda = None

    ev_ebitda = ev / ebitda[-1] if ev is not None and ebitda is not None else "N/A"

    return {
        "Enterprise Value": ev,
        "EV/EBITDA": ev_ebitda,
        "P/E Ratio": pe_ratio
    }

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

def plot_financials(financials, ticker):
    plt.figure(figsize=(10, 6))
    
    if "Revenue" in financials.columns:
        plt.plot(financials.index, financials["Revenue"], label="Revenue", marker="o")
    if "EBITDA" in financials.columns:
        plt.plot(financials.index, financials["EBITDA"], label="EBITDA", marker="o")
    if "EBIT" in financials.columns:
        plt.plot(financials.index, financials["EBIT"], label="EBIT", marker="o")

    plt.title(f"Financial Data Over Time for {ticker}")
    plt.xlabel("Year")
    plt.ylabel("Value (in billions)")
    plt.legend()
    st.pyplot(plt)

def p_and_l_page():
    st.title("Financial P&L and Valuation Dashboard")
    st.write("""
    Use this page to fetch key financial metrics (P&L) and valuation ratios for selected stocks using Yahoo Finance (yFinance).
    The following metrics will be extracted:
    - **P&L Metrics**: Revenue, COGS, EBITDA, EBIT, Net Income, R&D, S&GA, Revenue Growth
    - **Valuation Metrics**: EV/EBITDA and P/E Ratio
    """)

    st.subheader("Input Ticker Symbols")
    ticker_input = st.text_input("Enter stock ticker symbols (comma-separated, e.g., AAPL, MSFT, TSLA):", "AAPL")

    if st.button("Get Data"):
        with st.spinner("Fetching data..."):
            financials, valuations = get_financials_for_multiple(ticker_input)

            for ticker, data in financials.items():
                if isinstance(data, str): 
                    st.error(f"{ticker}: {data}")
                else:
                    st.subheader(f"Profit & Loss Statement for {ticker}")

                    st.dataframe(data.style.format(precision=2, na_rep='N/A').set_properties(**{
                        'background-color': 'lightcyan',
                        'color': 'black',
                        'border-color': 'gray',
                        'font-size': '14px'
                    }))
                    st.write("\n")

                    st.subheader(f"Valuation Metrics for {ticker}")
                    valuation_df = pd.DataFrame(valuations[ticker], index=[ticker])
                    st.table(valuation_df)


                    if st.button(f"Visualize {ticker} Financials Over Time"):
                        plot_financials(data, ticker)


p_and_l_page()
