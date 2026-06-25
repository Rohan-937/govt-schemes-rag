# ===== 1. Variables: koi type declaration nahi =====
name = "PM Scholarship"          # C++: string name = "...";
max_age = 35                     # C++: int
income_limit = 250000.0          # C++: double
is_active = True                 # C++: bool (capital T!)
print(name, max_age, is_active)

# ===== 2. f-strings: clean formatting =====
print(f"{name} ke liye max age {max_age} hai")

# ===== 3. Lists (C++ vector jaisa) =====
states = ["Rajasthan", "Delhi", "UP"]
states.append("Bihar")           # push_back
print(states[0], len(states))    # indexing + size()

# ===== 4. Dictionaries (C++ map jaisa) -- YE SABSE IMPORTANT =====
scheme = {
    "name": "PM Scholarship",
    "max_age": 35,
    "max_income": 250000,
    "states": ["All India"]
}
print(scheme["name"])            # key se access
scheme["category"] = "General"   # naya key add
print(scheme)

# ===== 5. Loops =====
for state in states:             # C++: for (auto s : states)
    print("State:", state)

for key, value in scheme.items():# dict pe loop
    print(key, "=>", value)

for i in range(3):               # 0,1,2  (C++: for(int i=0;i<3;i++))
    print("i =", i)

# ===== 6. Conditionals (braces nahi, indentation!) =====
user_age = 30
if user_age <= scheme["max_age"]:
    print("Eligible by age ✅")
else:
    print("Not eligible ❌")

# ===== 7. Functions =====
def is_eligible(age, max_age):   # C++: bool is_eligible(int age, int max_age)
    return age <= max_age

print(is_eligible(30, 35))       # True
print(is_eligible(40, 35))       # False

# ===== 8. List comprehension (bonus, bahut Pythonic) =====
young = [a for a in [20, 40, 25, 50] if a < 30]
print(young)                     # [20, 25]