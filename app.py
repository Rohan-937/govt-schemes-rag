import streamlit as st
from rag import search_schemes, generate_answer, schemes, is_eligible

st.set_page_config(page_title="Sarkari Yojana Sahayak", page_icon="🏛️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, .stTextInput, .stSelectbox, .stNumberInput, button {
    font-family: 'Inter', sans-serif;
}

.stApp { background-color: #FAFAFA; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 760px;
}

/* Main Header */
.hero {
    background: #FFFFFF;
    border: 1px solid #ECECEC;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.hero h1 { font-size: 28px; font-weight: 800; color: #111827; margin: 0 0 6px 0; }
.hero p  { font-size: 15px; color: #6B7280; margin: 0; line-height: 1.5; }

/* Section labels */
.section-label {
    font-size: 13px; font-weight: 600; color: #2563EB;
    text-transform: uppercase; letter-spacing: 0.5px; margin: 8px 0 4px 0;
}

/* Buttons */
.stButton > button {
    background: #2563EB; color: white; border: none;
    border-radius: 10px; padding: 10px 22px; font-weight: 600; font-size: 15px;
    transition: all 0.15s ease;
}
.stButton > button:hover { background: #1D4ED8; transform: translateY(-1px); }

/* Sidebar */
section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #ECECEC; }

/* Source Slides */
.chip-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.chip {
    display: inline-block; background: #EFF6FF; color: #2563EB;
    border: 1px solid #DBEAFE; border-radius: 999px; padding: 6px 14px;
    font-size: 13px; font-weight: 500; text-decoration: none;
}
.chip:hover { background: #DBEAFE; }

/* Scheme cards */
.scheme-card {
    background: #FFFFFF; border: 1px solid #ECECEC; border-radius: 12px;
    padding: 18px 20px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.scheme-card h4 { margin: 0 0 6px 0; font-size: 16px; color: #111827; font-weight: 700; }
.scheme-card p  { margin: 0 0 8px 0; font-size: 14px; color: #4B5563; line-height: 1.5; }
.scheme-card .benefit { font-size: 13px; color: #059669; font-weight: 600; }
.scheme-card a {
    display: inline-block; margin-top: 8px; font-size: 13px;
    color: #2563EB; font-weight: 600; text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🏛️ Government Scheme Finder</h1>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 👤 Aapki Profile")
    st.caption("Ye details eligibility check karne ke liye hain.")
    age        = st.number_input("Age", min_value=0, max_value=100, value=25)
    income     = st.number_input("Annual Income (₹)", min_value=0, value=200000, step=25000)
    gender     = st.selectbox("Gender", ["Male", "Female"])
    category   = st.selectbox("Category", ["General", "OBC", "SC", "ST"])
    state = st.selectbox("State", [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
        "Uttar Pradesh", "Uttarakhand", "West Bengal",
        "Andaman and Nicobar Islands", "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
        "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
    ])
    occupation = st.selectbox("Occupation",
                    ["Student", "Farmer", "Entrepreneur", "Worker", "Unemployed", "Street Vendor", "Artisan", "Other"])

profile = {
    "age": age, "income": income, "gender": gender,
    "category": category, "state": state, "occupation": occupation
}

st.markdown('<p class="section-label">💬 Ask the Question</p>', unsafe_allow_html=True)
query = st.text_input("query",
                      label_visibility="collapsed")

if st.button("🔍 Search", type="primary"):
    if not query.strip():
        st.warning("Please give an Input")
    else:
        with st.spinner("Searching Schemes..."):
            eligible = search_schemes(query, profile)
            result = generate_answer(query, eligible)

        with st.container(border=True):
            st.markdown("##### 📋 Jawab")
            st.write(result["answer"])
            if result["sources"]:
                chips = "".join(
                    f'<a class="chip" href="{s["link"]}" target="_blank">🔗 {s["name"]}</a>'
                    for s in result["sources"]
                )
                st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)


st.divider()
st.markdown('<p class="section-label">🎯 See all the Eligible Schemes</p>', unsafe_allow_html=True)

if st.button("Show all the schemes I am eligible for"):
    my_schemes = [s for s in schemes if is_eligible(profile, s)]
    if not my_schemes:
        st.info("No schemes found for this profile. Please try again after changing the profile")
    else:
        st.success(f"You are eligible for {len(my_schemes)} schemes:")
        for s in my_schemes:
            st.markdown(f"""
            <div class="scheme-card">
                <h4>📌 {s['name']}</h4>
                <p>{s['description']}</p>
                <div class="benefit">💰 {s['benefits']}</div>
                <a href="{s['link']}" target="_blank">Apply / Details →</a>
            </div>
            """, unsafe_allow_html=True)