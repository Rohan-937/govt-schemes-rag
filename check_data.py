import json   

with open("schemes.json", "r", encoding="utf-8") as f:
    schemes = json.load(f)


print(f"Total schemes loaded: {len(schemes)}")
print(f"Pehli scheme: {schemes[0]['name']}")

# Har scheme ka naam aur occupation print
for s in schemes:
    print(f"- {s['name']}  |  occupation: {s['eligibility']['occupation']}")