import streamlit as st

IS_DARK_THEME = True

st.title("Who is Peter Lynch?")

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.image("joost/assets/peter_lynch.png",caption="Peter Lynch during Fidelity Magellan Fund rule", width=300)

with col2:
    st.write(
        "Peter Lynch is a legendary investor who managed the Fidelity Magellan Fund from 1977 to 1990. "
        "During his tenure, the fund averaged a 29.2% annual return, consistently outperforming the S&P 500. "
        "Lynch is known for his investment philosophy of 'invest in what you know' and his ability to identify "
        "multibagger stocks. He is also the author of several books, including 'One Up on Wall Street' and 'Beating the Street'."
    )

    