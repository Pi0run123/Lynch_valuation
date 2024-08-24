import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
st.title("Calculation of Lynch Formula")

@st.dialog("Show the chart")
def show_stock_selector():
    st.write("Provide information to show chart")
    ticker = st.text_input("Ticker")
    date1 = st.date_input("Start date")
    date2 = st.date_input("End date")
    
    if st.button("Submit"):
        st.write("Thank you for providing the information.")
        data = yf.download(ticker, start=date1, end=date2)
        fig, ax = plt.subplots()
        ax.plot(data['Close'])
        ax.set_title(f"{ticker} Stock Prices")
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price")
        
        st.pyplot(fig)
@st.dialog("Calculate Lynch Formula")
def show_lynch_formula():
    st.write("Provide information to calculate the Lynch Formula")
    
    ticker = st.text_input("Ticker")
    
    if ticker:
        data = yf.Ticker(ticker)
        current_price = data.history(period='1d')['Close'][0]
        earnings = data.info['forwardEps']
        price_to_earnings = data.info['trailingPE']       
        peg_ratio = data.info['pegRatio']
        st.write(f"Lynch Formula for {ticker} is {peg_ratio}")
        st.write(f"Current price: {current_price:.2f}")
        st.write(f"Price-to-earnings ratio (PE): {price_to_earnings:.2f}")
        st.write(f"Earnings : {earnings:.2f}%")
        st.write(f"PEG ratio: {peg_ratio:.2f}")
        
        if peg_ratio == 1:
            st.write("The stock is fairly valued.")
        elif peg_ratio < 1:
            st.write("The stock is undervalued.")
        else:
            st.write("The stock is overvalued.")
    else:
        st.write("Please provide a valid ticker.")

if st.button("Insert stock info for show chart"):
    show_stock_selector()
if st.button("Calculate Lynch Formula"):
    show_lynch_formula()



st.write("Lynch Formula is calculated as follows:")
st.latex(r"PE = \frac{P}{E}")
st.latex(r"G = \frac{E}{P}")
st.latex(r"PEG = PE \times G")
st.write(
    "Where:\n"
    "- PE is the price-to-earnings ratio,\n"
    "- P is the stock price,\n"
    "- E is the earnings per share,\n"
    "- G is the earnings growth rate,\n"
    "- PEG is the PEG ratio."
)
st.write(
    "The Lynch Formula states that a stock is fairly valued when the PEG ratio is equal to 1. "
    "A PEG ratio of less than 1 indicates that the stock is undervalued, while a PEG ratio of greater than 1 indicates that the stock is overvalued."
)
st.write(
    "The Lynch Formula is a useful tool for investors to evaluate the valuation of a stock and identify potential investment opportunities."
)
st.write(
    "Please note that the Lynch Formula is just one of many tools that investors can use to evaluate stocks, and should be used in conjunction with other fundamental and technical analysis techniques."
)
st.write(
    "It is important for investors to conduct thorough research and due diligence before making investment decisions."
)
st.write(
    "For more information on the Lynch Formula and how to use it in your investment strategy, please refer to Peter Lynch's books 'One Up on Wall Street' and 'Beating the Street'."
)
st.write(
    "Happy investing!"
)
st.write(
    "Disclaimer: This information is for educational purposes only and should not be construed as financial advice. "
    "Investing in the stock market carries risks, and investors should consult with a financial advisor before making investment decisions."
)
st.write(
    "This app was created by Patryk Pioruński."
)
st.write(
    "Please fill out the form below to contact the author."
)





