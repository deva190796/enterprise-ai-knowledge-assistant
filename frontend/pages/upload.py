import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()
from api import upload_pdf

st.title("Upload PDF")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

pdf = st.file_uploader(
    "Choose PDF",
    type=["pdf"]
)

if st.button("Upload"):

    if pdf:

        response = upload_pdf(
            pdf,
            st.session_state["token"]
        )

        if response.status_code == 200:
            st.success("✅ PDF uploaded successfully!")

            st.balloons()
        else:
            st.error(response.text)