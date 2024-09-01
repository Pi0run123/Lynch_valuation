import streamlit as st

IS_DARK_THEME = True

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.title("Creator")

@st.dialog("Contact me")
def show_contact_form():
    st.write("Please fill out the form below to contact the author.")
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    if st.button("Submit"):
        st.write("Thank you for your message! The author will get back to you shortly.")

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.title("Patryk Pioruński", anchor=False)
    st.write("This app was created by Patryk Pioruński bla bla bla")

    if st.button("Contact me"):
        show_contact_form()