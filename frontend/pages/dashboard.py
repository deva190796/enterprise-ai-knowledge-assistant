import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# Protect Page
if "token" not in st.session_state:
    st.error("Please login first.")
    st.stop()

headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

response = requests.get(
    f"{BACKEND_URL}/dashboard/",
    headers=headers
)

if response.status_code != 200:
    st.error(response.json()["detail"])
    st.stop()

data = response.json()

st.title("📊 Dashboard")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.metric(
        "👤 Total Users",
        data["total_users"]
    )

with col2:
    st.metric(
        "📄 Total Documents",
        data["total_documents"]
    )

with col3:
    st.metric(
        "💬 Chat Sessions",
        data["total_chat_sessions"]
    )

with col4:
    st.metric(
        "🤖 Messages",
        data["total_messages"]
    )
st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("📄 Recent Documents")

    if data["recent_documents"]:

        for doc in data["recent_documents"]:
            st.write("•", doc["name"])

    else:
        st.info("No documents uploaded.")


with col2:

    st.subheader("💬 Recent Chats")

    if data["recent_chats"]:

        for chat in data["recent_chats"]:
            st.write("•", chat["title"])

    else:
        st.info("No chats available.")
st.divider()

st.subheader("📈 Analytics")

chart_data = {
    "Users": data["total_users"],
    "Documents": data["total_documents"],
    "Chat Sessions": data["total_chat_sessions"],
    "Messages": data["total_messages"]
}

st.bar_chart(chart_data)
st.subheader("📊 Distribution")

pie_data = {
    "Users": data["total_users"],
    "Documents": data["total_documents"],
    "Chats": data["total_chat_sessions"],
    "Messages": data["total_messages"]
}

st.write(pie_data)