from langchain_core.documents import Document

from app.services.pdf_service import extract_text
from app.services.text_splitter import split_text
from app.services.chroma_service import get_vector_store



def index_pdf(pdf_path: str, original_filename: str):

    text = extract_text(pdf_path)

    chunks = split_text(text)

    documents = [
        Document(
            page_content=chunk,
            metadata={
                "source": original_filename,
                "document": original_filename
            }
        )
        for chunk in chunks
    ]

    vector_store = get_vector_store()
    vector_store.add_documents(documents)

    return len(documents)