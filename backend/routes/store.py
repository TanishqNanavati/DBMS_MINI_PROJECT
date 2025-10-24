import requests
from bs4 import BeautifulSoup
from services.mysql_service import get_mysql_connection
from services.pg_service import insert_embedding
from services.embedding_service import generate_embedding
from utils.text_splitter import split_text

def store_website(category_name, url):
    # 1️⃣ Fetch HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else url
    content = " ".join([p.get_text() for p in soup.find_all("p")])

    if not content.strip():
        print(f"No content found at {url}")
        return

    # 2️⃣ Store in MySQL
    conn = get_mysql_connection(db_name=category_name)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pages (title, url, content) VALUES (%s, %s, %s)",
        (title, url, content)
    )
    conn.commit()
    record_id = cur.lastrowid
    cur.close()
    conn.close()

    # 3️⃣ Split content and generate embeddings
    chunks = split_text(content)
    embeddings = [generate_embedding(chunk) for chunk in chunks]

    for chunk, embedding in zip(chunks, embeddings):
        insert_embedding(category_name, record_id, chunk, embedding)

    print(f"Stored website '{url}' in {category_name} DB with {len(chunks)} embeddings.")
