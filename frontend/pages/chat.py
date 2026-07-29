import streamlit as st

from api import (
    ask_ai,
    get_chat_sessions,
    get_chat_messages,
    delete_chat,
    get_documents
)

st.title("Enterprise AI Knowledge Assistant")

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

# ---------------------------------------
# Sidebar - Chat History
# ---------------------------------------

st.sidebar.title("💬 Chats")

if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.session_id = None
    st.rerun()

response = get_chat_sessions(
    st.session_state["token"]
)

if response.status_code == 200:

    sessions = response.json()

    st.sidebar.divider()

    for session in sessions:

        col1, col2 = st.sidebar.columns([5, 1])

        with col1:

            if st.button(
                session["title"],
                key=f"chat_{session['id']}",
                use_container_width=True
            ):

                history = get_chat_messages(
                    session["id"],
                    st.session_state["token"]
                )

                if history.status_code == 200:

                    st.session_state.messages = history.json()
                    st.session_state.session_id = session["id"]

                    st.rerun()

        with col2:

            if st.button(
                "🗑️",
                key=f"delete_{session['id']}"
            ):

                delete_chat(
                    session["id"],
                    st.session_state["token"]
                )

                if st.session_state.session_id == session["id"]:
                    st.session_state.messages = []
                    st.session_state.session_id = None

                st.rerun()

# ---------------------------------------
# Load Documents
# ---------------------------------------

response = get_documents(
    st.session_state["token"]
)

documents = []

if response.status_code == 200:
    documents = response.json()

document_names = ["All Documents"]

for doc in documents:
    document_name = doc.get(
        "original_filename",
        doc["filename"]
    )
    document_names.append(document_name)

selected_document = st.selectbox(
    "📄 Select Document",
    document_names
)

if selected_document == "All Documents":
    selected_document = None

# ---------------------------------------
# Chat History
# ---------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask something about your uploaded documents..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):

        response = ask_ai(
            question=prompt,
            token=st.session_state["token"],
            document=selected_document,
            history=st.session_state.messages,
            session_id=st.session_state.session_id
        )

    if response.status_code == 200:

        data = response.json()

        st.session_state.session_id = data["session_id"]

        answer = data["answer"]
        sources = data["sources"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

            if sources:
                st.divider()
                st.markdown("#### Sources")

                for source in sources:
                    st.write(f"• {source}")

    else:
        st.error(response.text)