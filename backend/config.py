import os
from dotenv import load_dotenv
import mysql.connector
import psycopg2

# Load .env
load_dotenv()

# =========================
# MySQL Config (Root/Admin)
# =========================
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# =========================
# PostgreSQL Config (Central Vector DB)
# =========================
PG_HOST = os.getenv("PG_HOST")
PG_PORT = int(os.getenv("PG_PORT", 5432))
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")

# =========================
# MySQL Connection Helper
# =========================
def get_mysql_connection(db_name=None):
    """
    Returns a MySQL connection.
    If db_name is None, connects without specifying DB (useful for creating dynamic DBs)
    """
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=db_name  # Can be None
    )
    return conn

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
