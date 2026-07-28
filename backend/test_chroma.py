from app.services.pdf_service import extract_text
from app.services.text_splitter import split_text
from app.services.chroma_service import get_vector_store

pdf_path = "uploads/642af2f0-3aab-44fd-a02f-9378aefa858d_Deva_Kumar_Sattala_Resume1 (3).pdf"

text = extract_text(pdf_path)

chunks = split_text(text)

vector_store = get_vector_store()

vector_store.add_texts(chunks)

print(f"Stored {len(chunks)} chunks successfully!")