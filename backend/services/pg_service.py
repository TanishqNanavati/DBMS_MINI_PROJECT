from config import get_pg_connection

def insert_embedding(category_db, record_id, chunk_text, embedding):
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO embeddings (category_db, record_id, chunk_text, embedding)
        VALUES (%s, %s, %s, %s)
    """, (category_db, record_id, chunk_text, embedding))
    conn.commit()
    cur.close()
    conn.close()

def search_similar_embeddings(query_embedding, limit=5):
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT category_db, record_id, chunk_text, embedding <-> %s AS distance
        FROM embeddings
        ORDER BY distance ASC
        LIMIT %s
    """, (query_embedding, limit))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
