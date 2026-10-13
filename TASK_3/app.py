import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="RecoVerse AI", page_icon="🎯", layout="wide")

st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#0b1220,#172943)}
h1,h2,h3,p,label {color:white}
div.stButton>button {width:100%;border-radius:10px;font-weight:bold}
</style>
""", unsafe_allow_html=True)

st.title("🎯 RecoVerse AI")
st.write("Find movies, books and products based on your interests.")

# Sample datasets
movies = pd.DataFrame([
    ["3 Idiots","Comedy Drama","Indian",8.4],
    ["Dangal","Sports Drama","Indian",8.3],
    ["Drishyam","Crime Thriller","Indian",8.2],
    ["RRR","Action Drama","Indian",7.8],
    ["Interstellar","Sci-Fi Adventure","Hollywood",8.7],
    ["Inception","Sci-Fi Thriller","Hollywood",8.8],
    ["The Dark Knight","Action Crime","Hollywood",9.0],
    ["Titanic","Romance Drama","Hollywood",7.9]
], columns=["Name","Genre","Industry","Rating"])

books = pd.DataFrame([
    ["Atomic Habits","James Clear","Self Help"],
    ["Rich Dad Poor Dad","Robert Kiyosaki","Finance"],
    ["Wings of Fire","A.P.J. Abdul Kalam","Biography"],
    ["Harry Potter","J.K. Rowling","Fantasy"],
    ["Clean Code","Robert Martin","Programming"],
    ["The Alchemist","Paulo Coelho","Fiction"]
], columns=["Name","Author","Genre"])

products = pd.DataFrame([
    ["Gaming Laptop","Electronics Gaming",65000],
    ["Student Laptop","Electronics Education",40000],
    ["Headphones","Electronics Music",2500],
    ["Running Shoes","Sports Fitness",2200],
    ["Smart Watch","Electronics Fitness",3000],
    ["Python Book","Education Programming",600]
], columns=["Name","Category","Price"])

# Recommendation function
def get_recommendations(df, columns, query, favorite, count):
    if df.empty:
        return pd.DataFrame()

    text = df[columns].fillna("").astype(str).agg(" ".join, axis=1)
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(text)

    if favorite != "None":
        item = df[df["Name"] == favorite]
        if not item.empty:
            query += " " + item.iloc[0][columns].astype(str).str.cat(sep=" ")

    if not query.strip():
        return pd.DataFrame()

    scores = cosine_similarity(
        vectorizer.transform([query]), matrix
    ).flatten()

    result = df.copy()
    result["Similarity"] = scores

    if favorite != "None":
        result = result[result["Name"] != favorite]

    return result.sort_values("Similarity", ascending=False).head(count)

# Select category
category = st.selectbox("Choose Category", ["Movies", "Books", "Products"])

if category == "Movies":
    df = movies
    genres = sorted(set(g for x in df["Genre"] for g in x.split()))
    selected = st.multiselect("Choose genres", genres)
    industry = st.selectbox("Industry", ["All", "Indian", "Hollywood"])
    rating = st.slider("Minimum rating", 0.0, 10.0, 0.0, 0.5)
    favorite = st.selectbox("Favorite movie", ["None"] + df["Name"].tolist())
    columns = ["Genre", "Industry"]
    query = " ".join(selected)

    filtered = df[df["Rating"] >= rating].copy()
    if industry != "All":
        filtered = filtered[filtered["Industry"] == industry]
    if selected:
        filtered = filtered[filtered["Genre"].apply(
            lambda x: any(g in x.split() for g in selected)
        )]

elif category == "Books":
    df = books
    genres = sorted(df["Genre"].unique())
    selected = st.multiselect("Choose interests", genres)
    favorite = st.selectbox("Favorite book", ["None"] + df["Name"].tolist())
    columns = ["Name", "Author", "Genre"]
    query = " ".join(selected)
    filtered = df.copy()

    if selected:
        filtered = filtered[filtered["Genre"].isin(selected)]

else:
    df = products
    budget = st.slider("Maximum budget (₹)", 500, 100000, 30000, 500)
    categories = sorted(set(c for x in df["Category"] for c in x.split()))
    selected = st.multiselect("Choose interests", categories)
    favorite = st.selectbox("Favorite product", ["None"] + df["Name"].tolist())
    columns = ["Name", "Category"]
    query = " ".join(selected)
    filtered = df[df["Price"] <= budget].copy()

    if selected:
        filtered = filtered[filtered["Category"].apply(
            lambda x: any(c in x.split() for c in selected)
        )]

count = st.slider("Number of recommendations", 1, 5, 3)

if st.button("✨ Find Recommendations"):
    results = get_recommendations(filtered, columns, query, favorite, count)

    if results.empty:
        st.warning("Please select an interest or a favorite item.")
    else:
        st.subheader("Recommended for You")
        for _, item in results.iterrows():
            with st.container(border=True):
                st.subheader(item["Name"])

                for col in ["Genre", "Industry", "Rating", "Author", "Category", "Price"]:
                    if col in item.index:
                        value = item[col]
                        if col == "Price":
                            value = f"₹{value:,}"
                        st.write(f"**{col}:** {value}")

                st.progress(
                    min(float(item["Similarity"]), 1.0),
                    text="Content similarity"
                )

st.divider()
st.caption("Built with Python, Streamlit, Pandas and Scikit-learn.")

