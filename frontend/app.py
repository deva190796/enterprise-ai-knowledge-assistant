import streamlit as st

st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Initialize Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "token" not in st.session_state:
    st.session_state.token = None

# -----------------------------
# If not logged in -> Login Page
# -----------------------------
if not st.session_state.logged_in:
    st.switch_page("pages/login.py")
    st.stop()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🤖 Enterprise AI")

selected = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Upload PDF",
        "My Documents",
        "AI Chat"
    ]
)

if selected == "Dashboard":
    st.switch_page("pages/dashboard.py")

elif selected == "Upload PDF":
    st.switch_page("pages/upload.py")

elif selected == "My Documents":
    st.switch_page("pages/documents.py")

elif selected == "AI Chat":
    st.switch_page("pages/chat.py")

st.sidebar.divider()

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/login.py")
    
#https://enterprise-ai-knowledge-assistant-4.onrender.com/