import streamlit as st

IS_DARK_THEME = True

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

financial_data = st.Page(
    page = "pages/financial_data.py",
    title = "Profit & Loss"
)

pg = st.navigation(
    {
        "Info": [about_calc],
        "Lynch calc": [calculations, peter_lynch_page],
        "Analysis projects": [chart, financial_data],
        "Creator": [about_me]
    }
)

pg.run()