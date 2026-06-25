try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import json
import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv


load_dotenv() 
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

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
    if not (e["min_age"] <= profile["age"] <= e["max_age"]): return False
    if profile["income"] > e["max_income"]: return False
    if e["gender"] != "any" and e["gender"] != profile["gender"]: return False
    if "All" not in e["category"] and profile["category"] not in e["category"]: return False
    if "All India" not in e["states"] and profile["state"] not in e["states"]: return False
    if "All" not in e["occupation"] and profile["occupation"] not in e["occupation"]: return False
    return True

def search_schemes(query, profile, n_candidates=10):
    results = collection.query(query_texts=[query], n_results=n_candidates)
    return [scheme_by_id[sid] for sid in results["ids"][0]
            if is_eligible(profile, scheme_by_id[sid])]


def generate_answer(query, eligible_schemes):
    if not eligible_schemes:
        return {
            "answer": "Aapki profile ke hisaab se is sawaal ke liye koi eligible scheme nahi mili. "
                      "Profile ya sawaal thoda badal ke try karein.",
            "sources": []
        }

    context = ""
    for s in eligible_schemes:
        context += f"Scheme: {s['name']}\nDetails: {s['description']}\nBenefits: {s['benefits']}\n\n"

    prompt = f"""You are a helpful assistant for Indian government schemes.
Answer the user's question using ONLY the schemes listed below.
Rules:
- Mention each relevant scheme by its EXACT name.
- Explain in simple language why it fits the user.
- Do NOT mention or invent any scheme that is not in the list.
- If NONE of the schemes truly answer the question, say so honestly instead of guessing.

AVAILABLE SCHEMES:
{context}
USER QUESTION: {query}

Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    sources = [{"name": s["name"], "link": s["link"]} for s in eligible_schemes]

    return {"answer": response.choices[0].message.content, "sources": sources}

if __name__ == "__main__":
    user = {
        "age": 40, "income": 180000, "gender": "male",
        "category": "General", "state": "Bihar", "occupation": "Farmer"
    }
    query = "I need financial help and loans for farming"

    eligible = search_schemes(query, user)
    result = generate_answer(query, eligible)

    print(result["answer"])
    print("\n" + "=" * 50)
    print("📎 Sources (aap khud verify kar sakte ho):")
    for src in result["sources"]:
        print(f"  • {src['name']} → {src['link']}")