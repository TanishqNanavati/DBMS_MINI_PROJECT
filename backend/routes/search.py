from services.embedding_service import generate_embedding
from services.pg_service import search_similar_embeddings

def search_similar(query):
    query_emb = generate_embedding(query)
    results = search_similar_embeddings(query_emb)
    return [{"text": text, "similarity": round(1 - distance, 3)} for text, distance in results]
