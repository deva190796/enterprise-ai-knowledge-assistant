import streamlit as st


if st.session_state.get("logged_in", False):
    st.switch_page("pages/dashboard.py")
    st.stop()
from api import login

st.title("Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):

    response = login(email, password)

    if response.status_code == 200:
        data = response.json()

        st.session_state["token"] = data["access_token"]
        st.session_state["logged_in"] = True

        st.success("Login Successful!")
        st.switch_page("app.py")

    else:
        st.error(response.text)