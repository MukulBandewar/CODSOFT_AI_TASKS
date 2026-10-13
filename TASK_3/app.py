
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Recommendation System",
    page_icon="🎯",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #243b55);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATASET ----------------
data = {
    "Movies": [
        ("The Dark Knight", "Action Crime Thriller",
         "Batman fights crime and protects Gotham"),
        ("Avengers Endgame", "Action Adventure Sci-Fi",
         "Superheroes unite to save the universe"),
        ("Interstellar", "Sci-Fi Drama Adventure",
         "Astronauts travel through space to save humanity"),
        ("The Notebook", "Romance Drama",
         "A beautiful love story about relationships"),
        ("Titanic", "Romance Drama History",
         "Romantic story aboard a famous ship"),
        ("The Conjuring", "Horror Mystery Thriller",
         "A family faces paranormal activities"),
        ("The Hangover", "Comedy",
         "Friends experience hilarious adventures"),
        ("Finding Nemo", "Animation Adventure Family",
         "A fish travels the ocean to find his son"),
        ("The Matrix", "Sci-Fi Action",
         "A hacker discovers the truth about reality"),
        ("John Wick", "Action Crime Thriller",
         "A former assassin seeks revenge"),
    ],
    "Books": [
        ("Atomic Habits", "Self-Help Productivity",
         "Build good habits and improve daily life"),
        ("Rich Dad Poor Dad", "Finance Business",
         "Learn money management and financial literacy"),
        ("The Alchemist", "Fiction Adventure",
         "A young shepherd follows his dreams"),
        ("Harry Potter", "Fantasy Adventure",
         "A young wizard studies magic and fights evil"),
        ("The Psychology of Money", "Finance Psychology",
         "Understand behavior and decisions about money"),
        ("Deep Work", "Productivity Self-Help",
         "Improve focus and concentration"),
        ("Wings of Fire", "Biography Motivation",
         "The inspiring life story of APJ Abdul Kalam"),
        ("Ikigai", "Self-Help Philosophy",
         "Discover purpose and a meaningful life"),
        ("Think and Grow Rich", "Business Motivation",
         "Principles of success and achievement"),
        ("Sherlock Holmes", "Mystery Fiction",
         "A detective solves challenging mysteries"),
    ],
    "Products": [
        ("Gaming Laptop", "Electronics Gaming",
         "Powerful laptop for gaming and programming"),
        ("Wireless Headphones", "Electronics Music",
         "Wireless audio headphones with clear sound"),
        ("Smart Watch", "Electronics Fitness",
         "Track health activities and notifications"),
        ("Running Shoes", "Sports Fitness",
         "Comfortable shoes for running and exercise"),
        ("Python Programming Book", "Education Programming",
         "Learn Python coding and software development"),
        ("Mechanical Keyboard", "Electronics Gaming",
         "Mechanical keys for typing and gaming"),
        ("Yoga Mat", "Fitness Wellness",
         "Mat for yoga stretching and exercise"),
        ("Bluetooth Speaker", "Electronics Music",
         "Portable speaker for wireless music"),
        ("Travel Backpack", "Travel Accessories",
         "Spacious backpack for travel and daily use"),
        ("Digital Camera", "Electronics Photography",
         "Capture photographs and high-quality videos"),
    ]
}

# ---------------- RECOMMENDATION FUNCTION ----------------
def recommend_items(category, preference, favorite, count):
    df = pd.DataFrame(
        data[category],
        columns=["Name", "Genre", "Description"]
    )

    # Combine item features
    df["Features"] = (
        df["Genre"] + " " + df["Description"]
    )

    # TF-IDF feature extraction
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(df["Features"])

    # User preference vector
    user_text = preference

    if favorite != "None":
        favorite_description = df.loc[
            df["Name"] == favorite, "Features"
        ]

        if not favorite_description.empty:
            user_text += " " + favorite_description.iloc[0]

    user_vector = vectorizer.transform([user_text])

    # Cosine similarity with user preferences
    scores = cosine_similarity(user_vector, matrix).flatten()

    df["Score"] = scores

    # Do not recommend the selected favorite item itself
    if favorite != "None":
        df = df[df["Name"] != favorite]

    df = df.sort_values("Score", ascending=False)

    return df.head(count)


# ---------------- HEADER ----------------
st.title("🎯 Smart Recommendation System")
st.write(
    "Discover movies, books and products "
    "based on your interests."
)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Recommendation Settings")

category = st.sidebar.selectbox(
    "Select Category",
    ["Movies", "Books", "Products"]
)

category_preferences = {
    "Movies": [
        "Action", "Adventure", "Comedy", "Crime",
        "Drama", "Fantasy", "Horror", "Mystery",
        "Romance", "Sci-Fi", "Thriller", "Animation"
    ],
    "Books": [
        "Self-Help", "Productivity", "Finance",
        "Business", "Fiction", "Adventure", "Fantasy",
        "Biography", "Motivation", "Mystery",
        "Programming", "Psychology", "Philosophy"
    ],
    "Products": [
        "Electronics", "Gaming", "Music", "Fitness",
        "Sports", "Education", "Programming",
        "Travel", "Accessories", "Photography", "Wellness"
    ]
}

df_current = pd.DataFrame(
    data[category],
    columns=["Name", "Genre", "Description"]
)

selected_preferences = st.sidebar.multiselect(
    "Choose your interests",
    category_preferences[category]
)

favorite = st.sidebar.selectbox(
    "Choose a favorite item (optional)",
    ["None"] + df_current["Name"].tolist()
)

count = st.sidebar.slider(
    "Number of recommendations",
    3, 10, 5
)

# ---------------- MAIN CONTENT ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"✨ Explore {category}")
    st.write(
        "Choose your interests and discover "
        "items that match your preferences."
    )

    if st.button("🔍 Recommend For Me"):
        preference_text = " ".join(selected_preferences)

        if not preference_text and favorite == "None":
            st.warning(
                "Please select an interest or a favorite item."
            )
        else:
            results = recommend_items(
                category,
                preference_text,
                favorite,
                count
            )

            st.session_state["results"] = results
            st.session_state["result_category"] = category

with col2:
    st.subheader("📊 About the AI")
    st.write("**Algorithm:** Content-Based Filtering")
    st.write("**Feature extraction:** TF-IDF")
    st.write("**Similarity:** Cosine Similarity")
    st.write("**Categories:** Movies, Books, Products")

# ---------------- RESULTS ----------------
if (
    "results" in st.session_state
    and st.session_state.get("result_category") == category
):
    st.divider()
    st.subheader(f"🎁 Recommended {category}")

    results = st.session_state["results"]

    if results.empty:
        st.info("No matching items found.")
    else:
        cols = st.columns(2)

        for i, (_, item) in enumerate(results.iterrows()):
            with cols[i % 2]:
                with st.container(border=True):
                    st.markdown(f"### ⭐ {item['Name']}")
                    st.write(f"**Category:** {item['Genre']}")
                    st.write(item["Description"])

                    score = float(item["Score"])
                    st.progress(
                        max(0.0, min(1.0, score)),
                        text=f"Content similarity: {score:.0%}"
                    )

st.divider()
st.caption(
    "Built with Python, Streamlit, Pandas and Scikit-learn"
)

