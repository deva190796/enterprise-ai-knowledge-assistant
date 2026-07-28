from app.services.retrieval_service import search_documents

query = "What skills does the candidate have?"

results = search_documents(query)

print("=" * 70)

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 70)
    print(doc.page_content)