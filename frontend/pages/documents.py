import streamlit as st

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()
from api import get_documents, delete_document

st.title(" My Documents")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

response = get_documents(st.session_state["token"])

if response.status_code != 200:
    st.error(response.text)
    st.stop()

documents = response.json()

if len(documents) == 0:
    st.info("No documents uploaded.")
else:

    for doc in documents:

        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f" {doc['filename']}")

        with col2:
            if st.button("Delete", key=f"delete_{doc['id']}"):

                r = delete_document(
                    doc["id"],
                    st.session_state["token"]
                )

                if r.status_code == 200:
                    st.success("Deleted Successfully")
                    st.rerun()
                else:
                    st.error(r.text)