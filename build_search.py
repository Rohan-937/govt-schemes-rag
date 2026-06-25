import json
import chromadb
from chromadb.utils import embedding_functions

# 1. Schemes load 
with open("schemes.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

client = chromadb.PersistentClient(path="./chroma_db")

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(name="schemes", embedding_function=ef)

collection.upsert(
    documents=[s["description"] for s in schemes],   
    ids=[s["id"] for s in schemes],                  
    metadatas=[{"name": s["name"], "link": s["link"]} for s in schemes]
)
print(f"{collection.count()} schemes indexed ✅\n")

query = "free gas connection"
results = collection.query(query_texts=[query], n_results=3)

print(f"Query: {query}\n")
for meta, dist in zip(results["metadatas"][0], results["distances"][0]):
    print(f"• {meta['name']}  (distance: {dist:.3f})")