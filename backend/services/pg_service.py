from config import get_pg_connection

def insert_embedding(record_text, embedding):
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO embeddings (record_text, embedding)
        VALUES (%s, %s)
    """, (record_text, embedding))
    conn.commit()
    cur.close()
    conn.close()

def search_similar_embeddings(query_embedding, limit=5):
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT record_text, embedding <-> %s AS distance
        FROM embeddings
        ORDER BY distance ASC
        LIMIT %s
    """, (query_embedding, limit))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
