import os

from langchain_chroma import Chroma

from app.services.embedding_service import get_embedding_model


CHROMA_DB_PATH = "app/chroma_db"


def get_vector_store():

    embeddings = get_embedding_model()

    vector_store = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )

    return vector_store