from app.services.chroma_service import get_vector_store


def search_documents(
    query: str,
    document: str | None = None,
    k: int = 10
):
    vector_store = get_vector_store()

    if document:
        results = vector_store.similarity_search(
            query=query,
            k=k,
            filter={
                "source": document
            }
        )
    else:
        results = vector_store.similarity_search(
            query=query,
            k=k
        )

    return results