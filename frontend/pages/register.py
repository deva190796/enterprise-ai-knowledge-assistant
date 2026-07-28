import streamlit as st


if st.session_state.get("logged_in", False):
    st.switch_page("pages/dashboard.py")
    st.stop()

from api import register

st.title("Register")

full_name = st.text_input("Full Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Register"):

    response = register(full_name, email, password)

    if response.status_code == 200:
        st.success("Registration Successful")
    else:
        st.error(response.text)