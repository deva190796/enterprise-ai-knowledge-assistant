from app.services.pdf_service import extract_text
from app.services.text_splitter import split_text

pdf_path = "uploads/642af2f0-3aab-44fd-a02f-9378aefa858d_Deva_Kumar_Sattala_Resume1 (3).pdf"

text = extract_text(pdf_path)

chunks = split_text(text)

print("=" * 60)
print(f"Total Chunks: {len(chunks)}")
print("=" * 60)

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}")
    print("-" * 40)
    print(chunk)