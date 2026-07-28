from app.services.pdf_service import extract_text

text = extract_text(
    "uploads/642af2f0-3aab-44fd-a02f-9378aefa858d_Deva_Kumar_Sattala_Resume1 (3).pdf"
)

print(text)