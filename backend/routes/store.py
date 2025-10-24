import requests
from bs4 import BeautifulSoup
from services.pg_service import insert_embedding
from services.embedding_service import generate_embedding
from utils.text_splitter import split_text

def store_website(url):
    # Fetch HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    content = " ".join([p.get_text() for p in soup.find_all("p")])
    chunks = split_text(content)

    for chunk in chunks:
        embedding = generate_embedding(chunk)
        insert_embedding(chunk, embedding)

    print(f"Stored website '{url}' with {len(chunks)} embeddings.")
