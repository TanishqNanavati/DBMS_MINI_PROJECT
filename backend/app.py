from routes.store import store_website
from routes.search import search_similar
from services.mysql_service import create_category_db

# Create MySQL DB for category if not exists
create_category_db("school")

# Store a website
store_website("school", "https://en.wikipedia.org/wiki/Computer_science")

# Search semantically
results = search_similar("school", "What is computing?")
for r in results:
    print(r)
