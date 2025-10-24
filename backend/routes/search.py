from services.embedding_service import generate_embedding
from services.pg_service import search_similar_embeddings
from services.mysql_service import get_mysql_connection

def search_similar(category_name, query, limit=5):
    # Generate embedding for the query
    query_emb = generate_embedding(query)

    # Fetch similar chunks from pgvector
    results = search_similar_embeddings(query_emb, limit=limit)

    final_results = []
    for cat_db, record_id, chunk_text, distance in results:
        if cat_db == category_name:
            conn = get_mysql_connection(db_name=cat_db)
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT title, url FROM pages WHERE id = %s", (record_id,))
            page = cur.fetchone()
            cur.close()
            conn.close()
            final_results.append({
                "title": page["title"],
                "url": page["url"],
                "chunk": chunk_text,
                "similarity": round(1 - distance, 3)
            })

    return final_results
