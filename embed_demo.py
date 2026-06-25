from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

vec = model.encode("scholarship for students")
print("Vector me kitne numbers:", len(vec))   
print("Pehle 5 numbers:", vec[:5])

a = model.encode("money help for farmers")
b = model.encode("financial support for agriculture")   
c = model.encode("pizza recipe with cheese")           

print("Similar pair similarity :", round(util.cos_sim(a, b).item(), 3))   # high
print("Unrelated pair similarity:", round(util.cos_sim(a, c).item(), 3))  # low