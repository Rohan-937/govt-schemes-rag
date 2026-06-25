import json
import chromadb
from chromadb.utils import embedding_functions

with open("schemes.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)

scheme_by_id = {s["id"]: s for s in schemes}

client = chromadb.PersistentClient(path="./chroma_db")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="schemes", embedding_function=ef)

if collection.count() == 0:
    collection.upsert(
        documents=[s["description"] for s in schemes],
        ids=[s["id"] for s in schemes],
        metadatas=[{"name": s["name"], "link": s["link"]} for s in schemes]
    )


def is_eligible(profile, scheme):
    e = scheme["eligibility"]

    # Age range 
    if not (e["min_age"] <= profile["age"] <= e["max_age"]):
        return False
    # Income limit 
    if profile["income"] > e["max_income"]:
        return False
    if e["gender"] != "any" and e["gender"] != profile["gender"]:
        return False
    if "All" not in e["category"] and profile["category"] not in e["category"]:
        return False
    if "All India" not in e["states"] and profile["state"] not in e["states"]:
        return False
    if "All" not in e["occupation"] and profile["occupation"] not in e["occupation"]:
        return False

    return True   # saare rules paas matlab eligible

def search_schemes(query, profile, n_candidates=10):
    results = collection.query(query_texts=[query], n_results=n_candidates)
    eligible = []
    for sid in results["ids"][0]:          
        scheme = scheme_by_id[sid]         
        if is_eligible(profile, scheme):  
            eligible.append(scheme)
    return eligible

user = {
    "age": 40, "income": 180000, "gender": "male",
    "category": "General", "state": "Bihar", "occupation": "Farmer"
}
query = "financial help and loans"

print("=== BINA filter (pure RAG) ===")
raw = collection.query(query_texts=[query], n_results=5)
for meta in raw["metadatas"][0]:
    print("  •", meta["name"])

print("\n=== FILTER ke saath (hamara smart version) ===")
for s in search_schemes(query, user):
    print("  •", s["name"], "→ eligible ✅")