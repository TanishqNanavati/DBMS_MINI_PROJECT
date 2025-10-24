import os
from dotenv import load_dotenv
import psycopg2

# Load .env
load_dotenv()

# =========================
# PostgreSQL Config (Central Vector DB)
# =========================
PG_HOST = os.getenv("PG_HOST")
PG_PORT = int(os.getenv("PG_PORT", 5432))
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")

# =========================
# PostgreSQL Connection Helper
# =========================
def get_pg_connection():
    """
    Returns a PostgreSQL connection to vector_db
    """
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        dbname=PG_DB
    )
    return conn
