from app.services.embedding_service import get_embedding_model

embedding_model = get_embedding_model()

embedding = embedding_model.embed_query("Hello World")

print("=" * 50)
print("Embedding Generated Successfully!")
print("=" * 50)
print(f"Embedding Length: {len(embedding)}")
print(embedding[:10])