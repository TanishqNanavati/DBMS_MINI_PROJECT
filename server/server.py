
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
from sentence_transformers import SentenceTransformer

# Initialize
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model
model = None

def get_model():
    global model
    if model is None:
        print("Loading model...")
        model = SentenceTransformer('all-mpnet-base-v2')
        print("Model loaded!")
    return model

def get_db():
    return psycopg2.connect(
        host="172.17.0.3",
        database="browser_history",
        user="postgres",
        password="postgres"
    )

# Models
class PageIngest(BaseModel):
    profile_id: int
    url: str
    title: str
    content: str

class SearchRequest(BaseModel):
    query: str
    profile_id: int

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/profiles")
def list_profiles():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM profiles ORDER BY id")
    profiles = cur.fetchall()
    cur.close()
    conn.close()
    return profiles

@app.post("/profiles")
def create_profile(name: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO profiles (name) VALUES (%s) RETURNING *", (name,))
    profile = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return profile

@app.post("/ingest")
def ingest_page(data: PageIngest):
    # Hash content
    content_hash = hashlib.md5(data.content.encode()).hexdigest()
    
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if exists
    cur.execute("SELECT id FROM pages WHERE content_hash = %s", (content_hash,))
    existing = cur.fetchone()
    if existing:
        cur.close()
        conn.close()
        return {"message": "already indexed", "page_id": existing['id']}
    
    # Insert page
    cur.execute(
        "INSERT INTO pages (profile_id, url, title, content_hash) VALUES (%s, %s, %s, %s) RETURNING id",
        (data.profile_id, data.url, data.title, content_hash)
    )
    page_id = cur.fetchone()['id']
    
    # Chunk text (simple 500 char chunks)
    chunks = []
    text = data.content
    chunk_size = 500
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    # Generate embeddings
    embeddings = get_model().encode(chunks, normalize_embeddings=True)
    
    # Insert chunks
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        embedding_list = embedding.tolist()
        cur.execute(
            "INSERT INTO page_chunks (page_id, chunk_index, chunk_text, token_count, embedding) VALUES (%s, %s, %s, %s, %s)",
            (page_id, idx, chunk, len(chunk)//4, embedding_list)
        )
    
    conn.commit()
    cur.close()
    conn.close()
    
    return {"message": "success", "page_id": page_id, "chunks": len(chunks)}

@app.post("/search")
def search(req: SearchRequest):
    # Generate query embedding
    query_embedding = get_model().encode([req.query], normalize_embeddings=True)[0].tolist()
    
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Search
    cur.execute("""
        SELECT 
            p.id, p.url, p.title, pc.chunk_text,
            1 - (pc.embedding <=> %s::vector) as similarity
        FROM page_chunks pc
        JOIN pages p ON pc.page_id = p.id
        WHERE p.profile_id = %s
        ORDER BY pc.embedding <=> %s::vector
        LIMIT 10
    """, (query_embedding, req.profile_id, query_embedding))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    # Group by page
    pages = {}
    for row in results:
        pid = row['id']
        if pid not in pages:
            pages[pid] = {
                'page_id': pid,
                'url': row['url'],
                'title': row['title'],
                'snippet': row['chunk_text'][:200],
                'similarity': row['similarity']
            }
    
    return list(pages.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)