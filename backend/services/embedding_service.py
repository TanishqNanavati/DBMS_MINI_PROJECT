import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load .env variables
load_dotenv()

# Load model name from .env, default to "all-mpnet-base-v2" if not set
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-mpnet-base-v2")

# Load model once
model = SentenceTransformer(EMBEDDING_MODEL)

def generate_embedding(text):
    """
    Generate a 768-dimensional embedding for a text using Sentence Transformers.
    """
    embedding = model.encode(text)
    return embedding.tolist()  # Convert to list so it can be stored in PostgreSQL
