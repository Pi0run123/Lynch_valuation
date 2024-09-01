import streamlit as st

IS_DARK_THEME = True

st.markdown("""
    <style>
        .css-1d391kg { /* Adjust the selector as needed */
            padding-top: 100px; /* Adjust the height */
        }
    </style>
    """, unsafe_allow_html=True)


about_calc = st.Page(
    page = "pages/about_calc.py",
    title = "About Formula",
    default=True
)

about_me = st.Page(
    page = "pages/about_me.py",
    title = "About Author"
)

calculations = st.Page(
    page = "pages/calculations.py",
    title = "Lynch Formula"
)

peter_lynch_page = st.Page(
    page = "pages/peter_lynch.py",
    title = "Story of Peter Lynch"
)

chart = st.Page(
    page = "pages/chart.py",
    title = "Stock Chart"
)

pg = st.navigation(
    {
        "Info": [about_calc],
        "Projects": [calculations, peter_lynch_page, chart],
        "Creator": [about_me]
    }
)

pg.run()