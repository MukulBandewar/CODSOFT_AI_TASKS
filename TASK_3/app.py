import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="RecoVerse AI", page_icon="🎯", layout="wide")

st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0b1220,#172943);color:white}
h1,h2,h3,p,label{color:white}
.hero{padding:25px;border-radius:18px;background:linear-gradient(120deg,#273c75,#192a56);text-align:center}
div.stButton>button{width:100%;min-height:42px;border-radius:10px;font-weight:bold}
</style>
""", unsafe_allow_html=True)

# ---------------- DATASETS ----------------
movies = [
("3 Idiots","Indian","Comedy Drama","Hindi",8.4,"Check current OTT catalogue","Hindi","College, friendship, engineering"),
("Dangal","Indian","Sports Drama","Hindi",8.3,"Check current OTT catalogue","Hindi","Wrestling, family, motivation"),
("Drishyam","Indian","Crime Thriller","Hindi",8.2,"Check current OTT catalogue","Hindi","Mystery, crime, suspense"),
("12th Fail","Indian","Drama Motivation","Hindi",8.8,"Check current OTT catalogue","Hindi","Education, UPSC, determination"),
("RRR","Indian","Action Drama","Telugu",7.8,"Check current OTT catalogue","Telugu, Hindi","Action, friendship, history"),
("Kantara","Indian","Action Thriller","Kannada",8.2,"Check current OTT catalogue","Kannada, Hindi","Folklore, mystery, action"),
("Interstellar","Hollywood","Sci-Fi Adventure","English",8.7,"Check current OTT catalogue","English","Space, science, survival"),
("Inception","Hollywood","Sci-Fi Thriller","English",8.8,"Check current OTT catalogue","English","Dreams, mind, science fiction"),
("The Dark Knight","Hollywood","Action Crime","English",9.0,"Check current OTT catalogue","English","Batman, crime, justice"),
("Titanic","Hollywood","Romance Drama","English",7.9,"Check current OTT catalogue","English","Romance, ship, history")
]
movie_df = pd.DataFrame(movies, columns=[
    "Name","Industry","Genre","Language","IMDb Rating",
    "OTT Information","Dubbed Languages","Description"
])

books = [
("Atomic Habits","James Clear","Self Help Productivity","Habits, discipline, personal growth"),
("The Psychology of Money","Morgan Housel","Finance Psychology","Money, investing, financial behaviour"),
("Wings of Fire","A. P. J. Abdul Kalam","Biography Motivation","Science, India, determination"),
("The Alchemist","Paulo Coelho","Fiction Adventure","Dreams, journey, self discovery"),
("Harry Potter","J. K. Rowling","Fantasy Adventure","Magic, friendship, wizard school"),
("Clean Code","Robert C. Martin","Programming Education","Software development, coding, best practices"),
("Sapiens","Yuval Noah Harari","History Science","Human history, civilization, evolution"),
("Deep Work","Cal Newport","Productivity Education","Focus, concentration, deep learning")
]
book_df = pd.DataFrame(books, columns=["Name","Author","Genre","Description"])

products = [
("Gaming Laptop","Electronics Gaming","Gaming, coding, powerful processor",65000),
("Student Laptop","Electronics Education","Study, coding, college, productivity",40000),
("Wireless Headphones","Electronics Music","Music, wireless audio, travel",2500),
("Smart Watch","Electronics Fitness","Fitness, notifications, health tracking",3000),
("Running Shoes","Sports Fitness","Running, walking, exercise",2200),
("Python Programming Book","Education Programming","Python, coding, learning",600),
("Power Bank","Electronics Accessories","Charging, smartphone, travel",1200),
("Tablet","Electronics Education","Reading, studying, video, productivity",18000)
]
product_df = pd.DataFrame(products, columns=["Name","Category","Description","Price (INR)"])

# ---------------- RECOMMENDATION ENGINE ----------------
def recommend(df, columns, query, favorite, count):
    if df.empty:
        return pd.DataFrame()

    text = df[columns].fillna("").astype(str).agg(" ".join, axis=1)
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(text)

    if favorite != "None":
        item = df[df["Name"] == favorite]
        if not item.empty:
            query += " " + item.iloc[0][columns].astype(str).str.cat(sep=" ")

    if not query.strip():
        return pd.DataFrame()

    scores = cosine_similarity(vectorizer.transform([query]), matrix).ravel()
    result = df.copy()
    result["Similarity"] = scores

    if favorite != "None":
        result = result[result["Name"] != favorite]

    return result.sort_values("Similarity", ascending=False).head(count)

def show_results(results, category):
    if results.empty:
        st.warning("No matching items found. Try changing your filters or select a favorite.")
        return

    st.subheader("✨ Your Recommendations")
    for _, item in results.iterrows():
        with st.container(border=True):
            st.markdown(f"### {item['Name']}")

            fields = {
                "Movies": ["Industry","Genre","Language","IMDb Rating",
                           "OTT Information","Dubbed Languages","Description"],
                "Books": ["Author","Genre","Description"],
                "Products": ["Category","Price (INR)","Description"]
            }[category]

            for field in fields:
                if field in item.index:
                    value = item[field]
                    if field == "Price (INR)":
                        value = f"₹{value:,}"
                    if field == "IMDb Rating":
                        value = f"{value}/10 (approx.)"
                    st.write(f"**{field}:** {value}")

            st.progress(min(float(item["Similarity"]), 1.0),
                        text="Content similarity (not accuracy)")

# ---------------- HOME PAGE ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>🎯 RecoVerse AI</h1>
        <h3>Your Personal Recommendation Hub</h3>
        <p>Discover movies, books and products based on your interests.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.subheader("What would you like to discover?")
    c1, c2, c3 = st.columns(3)

    for col, name, emoji, desc in [
        (c1,"Movies","🎬","Indian cinema and Hollywood"),
        (c2,"Books","📚","Fiction, technology and self-help"),
        (c3,"Products","🛍️","Technology, education and fitness")
    ]:
        with col:
            with st.container(border=True):
                st.markdown(f"## {emoji} {name}")
                st.write(desc)
                if st.button(f"Explore {name}", key=f"home_{name}"):
                    st.session_state.page = name
                    st.rerun()

else:
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    category = st.session_state.page
    st.title({"Movies":"🎬 Movie Recommendations",
              "Books":"📚 Book Recommendations",
              "Products":"🛍️ Product Recommendations"}[category])

    if category == "Movies":
        df = movie_df
        c1, c2 = st.columns(2)

        with c1:
            industry = st.selectbox("Cinema", ["All","Indian","Hollywood"])
            genres = sorted(set(g for x in df["Genre"] for g in x.split()))
            selected = st.multiselect("Genres", genres)
            languages = st.multiselect("Original language", sorted(df["Language"].unique()))

        with c2:
            rating = st.slider("Minimum IMDb rating (approx.)", 0.0, 10.0, 0.0, 0.5)
            dubbed = st.selectbox("Dubbed-language preference",
                                  ["Any","Hindi","Tamil","Telugu","Kannada","Malayalam","English"])
            favorite = st.selectbox("Favorite movie", ["None"] + df["Name"].tolist())

        count = st.slider("Number of recommendations", 3, 8, 5)
        filtered = df[df["IMDb Rating"] >= rating].copy()

        if industry != "All":
            filtered = filtered[filtered["Industry"] == industry]
        if languages:
            filtered = filtered[filtered["Language"].isin(languages)]
        if selected:
            filtered = filtered[filtered["Genre"].apply(
                lambda x: any(g in x.split() for g in selected))]
        if dubbed != "Any":
            filtered = filtered[filtered["Dubbed Languages"].str.contains(
                dubbed, case=False, na=False)]

        query = " ".join(selected + ([] if dubbed == "Any" else [dubbed]))
        columns = ["Genre","Description","Language","Industry","Dubbed Languages"]

        if st.button("✨ Find Movies"):
            show_results(recommend(filtered, columns, query, favorite, count), category)

        st.info("OTT and dubbed-audio information may vary by region and can change")

    elif category == "Books":
        df = book_df
        authors = st.multiselect("Authors (optional)", sorted(df["Author"].unique()))
        genres = sorted(set(g for x in df["Genre"] for g in x.split()))
        selected = st.multiselect("Book interests", genres)
        favorite = st.selectbox("Favorite book", ["None"] + df["Name"].tolist())
        count = st.slider("Number of recommendations", 3, 8, 5)

        filtered = df.copy()
        if authors:
            filtered = filtered[filtered["Author"].isin(authors)]
        if selected:
            filtered = filtered[filtered["Genre"].apply(
                lambda x: any(g in x.split() for g in selected))]

        if st.button("✨ Find Books"):
            show_results(recommend(filtered, ["Name","Author","Genre","Description"],
                                   " ".join(selected), favorite, count), category)

    else:
        df = product_df
        categories = sorted(set(g for x in df["Category"] for g in x.split()))
        selected = st.multiselect("Product interests", categories)
        budget = st.slider("Maximum budget (₹)", 500, 100000, 30000, 500)
        favorite = st.selectbox("Favorite product", ["None"] + df["Name"].tolist())
        count = st.slider("Number of recommendations", 3, 8, 5)

        filtered = df[df["Price (INR)"] <= budget].copy()
        if selected:
            filtered = filtered[filtered["Category"].apply(
                lambda x: any(g in x.split() for g in selected))]

        if st.button("✨ Find Products"):
            show_results(recommend(filtered, ["Name","Category","Description"],
                                   " ".join(selected), favorite, count), category)

st.divider()
st.caption("Developer - Mukul Bandewar | RecoVerse AI | Python • Streamlit • Pandas ")
