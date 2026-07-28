import os

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

from app.services.retrieval_service import search_documents

load_dotenv(override=True)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def ask_question(
    question: str,
    document: str | None = None,
    history: list = []
):

    docs = search_documents(
        query=question,
        document=document
    )

    if not docs:
        return {
            "answer": "I couldn't find any relevant information in the uploaded documents.",
            "sources": []
        }

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    conversation = ""

    for msg in history[-6:]:
            role = msg.role.capitalize()
            content = msg.content
            conversation += f"{role}: {content}\n"

    prompt = f"""
You are an AI assistant.

Use the conversation history to understand follow-up questions.

Answer ONLY from the provided document context.

If the answer is not present in the context, reply:
"I couldn't find that information in the uploaded documents."

Conversation History:
{conversation}

Document Context:
{context}

Current Question:
{question}

Answer:
"""

    sources = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")

        if source not in sources:
            sources.append(source)

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return {
            "answer": response.text,
            "sources": sources
        }

    except ClientError as e:
        return {
            "answer": f"Gemini API Error: {e}",
            "sources": sources
        }

    except Exception as e:
        return {
            "answer": f"Unexpected Error: {e}",
            "sources": sources
        }