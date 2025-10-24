from routes.store import store_website
from routes.search import search_similar

# Category name in pgvector (just a label, no MySQL DB)
category_name = "school"

# Store a website: fetch content, split into chunks, generate embeddings, insert into PG
store_website(category_name, "https://en.wikipedia.org/wiki/Computer_science")

# Search semantically in that category
results = search_similar(category_name, "What is computing?")
for r in results:
    print(r)
