

import requests




import os

BASE_URL = os.getenv(
    "BACKEND_URL",
    "https://enterprise-ai-knowledge-assistant-4sye.onrender.com"
)

def register(full_name, email, password):
    return requests.post(
        f"{BASE_URL}/users/",
        json={
            "full_name": full_name,
            "email": email,
            "password": password
        }
    )


def login(email, password):
    return requests.post(
        f"{BASE_URL}/users/login",
        data={
            "username": email,
            "password": password
        }
    )


def upload_pdf(file, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    files = {
        "file": (file.name, file, "application/pdf")
    }

    return requests.post(
        f"{BASE_URL}/documents/upload",
        headers=headers,
        files=files
    )


def get_documents(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{BASE_URL}/documents/",
        headers=headers
    )


def delete_document(document_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.delete(
        f"{BASE_URL}/documents/{document_id}",
        headers=headers
    )


def ask_ai(
    question,
    token,
    document=None,
    history=None,
    session_id=None
):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    if history is None:
        history = []

    return requests.post(
        f"{BASE_URL}/chat/",
        headers=headers,
        json={
            "question": question,
            "document": document,
            "history": history,
            "session_id": session_id
        }
    )
import inspect

print("API FILE LOADED")
print(inspect.signature(ask_ai))

def get_chat_sessions(token):

    response = requests.get(
        f"{BASE_URL}/chat/sessions",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def get_chat_messages(session_id, token):

    response = requests.get(
        f"{BASE_URL}/chat/sessions/{session_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response


def delete_chat(session_id, token):

    response = requests.delete(
        f"{BASE_URL}/chat/sessions/{session_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return response