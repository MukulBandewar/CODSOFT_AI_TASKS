
import streamlit as st
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="RecoVerse AI",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0b1220,#172943);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
h1,h2,h3,h4,p,label {
    color: white !important;
}
.block-container {
    max-width: 1250px;
    padding: 2rem 2rem 3rem;
}
.hero {
    padding: 30px 18px;
    border-radius: 18px;
    background: linear-gradient(120deg,#273c75,#192a56);
    text-align: center;
    border: 1px solid #40558c;
}
.hero h1 {
    font-size: clamp(2rem,5vw,3.2rem);
}
.hero p {
    color: #dbeafe !important;
}
.stButton > button {
    width: 100%;
    min-height: 44px;
    border-radius: 11px;
    background: linear-gradient(90deg,#4f46e5,#9333ea);
    color: white !important;
    border: 1px solid #6366f1;
    font-weight: 650;
}
.stButton > button:hover {
    border-color: #c4b5fd;
    box-shadow: 0 4px 14px #6366f155;
}
div[data-testid="stMetric"] {
    background: #17243a;
    border: 1px solid #40558c;
    border-radius: 13px;
    padding: 12px;
}
div[data-testid="stMetricLabel"],
div[data-testid="stMetricValue"] {
    color: white !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #334b70;
    border-radius: 14px;
}
[data-testid="stSidebar"] {
    background: #0c1729;
}
[data-testid="stExpander"] {
    border-color: #334b70;
    border-radius: 12px;
}
hr {
    border-color: #334155;
}
@media(max-width:768px) {
    .block-container {
        padding: 1rem .8rem 2rem !important;
    }
    .hero {
        padding: 22px 12px;
        border-radius: 14px;
    }
    .hero h1 {
        font-size: 2rem;
    }
    .hero h3 {
        font-size: 1rem;
    }
    .hero p {
        font-size: .9rem;
    }
    h1 {
        font-size: 1.7rem !important;
    }
    h2 {
        font-size: 1.4rem !important;
    }
    h3 {
        font-size: 1.15rem !important;
    }
    div[data-testid="stMetric"] {
        padding: 8px 5px;
    }
    div[data-testid="stMetricLabel"] {
        font-size: .75rem !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.25rem !important;
    }
    .stButton > button {
        font-size: .9rem;
        min-height: 44px;
    }
}
@media(max-width:380px) {
    .block-container {
        padding-left: .55rem !important;
        padding-right: .55rem !important;
    }
    .hero h1 {
        font-size: 1.7rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.05rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent


def load_csv(filename, required_columns):
    path = BASE_DIR / filename

    if not path.exists():
        st.error(f"Dataset file not found: {filename}")
        st.info("Keep the CSV file in the same folder as app.py.")
        st.stop()

    try:
        df = pd.read_csv(path)
    except Exception as error:
        st.error(f"Could not read {filename}: {error}")
        st.stop()

    df.columns = df.columns.str.strip().str.lower()

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(
            f"{filename} is missing these columns: "
            + ", ".join(missing)
        )
        st.stop()

    if df.empty:
        st.error(f"{filename} has no data.")
        st.stop()

    return df.fillna("")


movie_df = load_csv(
    "trending_movies_2026.csv",
    [
        "item_id",
        "title",
        "genre",
        "release_year",
        "average_rating",
        "trending_score",
        "global_views_millions"
    ]
)

book_df = load_csv(
    "trending_books_2026.csv",
    [
        "item_id",
        "title",
        "author",
        "category",
        "rating",
        "purchase_count",
        "stock_status"
    ]
)

product_df = load_csv(
    "trending_products_2026.csv",
    [
        "item_id",
        "product_name",
        "category",
        "rating",
        "click_through_rate",
        "conversion_rate"
    ]
)


movie_df = movie_df.rename(columns={
    "title": "Name",
    "genre": "Genre",
    "release_year": "Release Year",
    "average_rating": "IMDb Rating",
    "trending_score": "Trending Score",
    "global_views_millions": "Global Views (Millions)"
})

book_df = book_df.rename(columns={
    "title": "Name",
    "author": "Author",
    "category": "Genre",
    "rating": "Rating",
    "purchase_count": "Purchase Count",
    "stock_status": "Stock Status"
})

product_df = product_df.rename(columns={
    "product_name": "Name",
    "category": "Category",
    "rating": "Rating",
    "click_through_rate": "Click Through Rate",
    "conversion_rate": "Conversion Rate"
})


def to_number(df, columns):
    for column in columns:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        ).fillna(0)
    return df


movie_df = to_number(movie_df, [
    "Release Year",
    "IMDb Rating",
    "Trending Score",
    "Global Views (Millions)"
])
movie_df["Description"] = movie_df["Genre"].astype(str)

book_df = to_number(book_df, [
    "Rating",
    "Purchase Count"
])
book_df["Description"] = (
    book_df["Genre"].astype(str) + " " +
    book_df["Author"].astype(str)
)

product_df = to_number(product_df, [
    "Rating",
    "Click Through Rate",
    "Conversion Rate"
])
product_df["Description"] = product_df["Category"].astype(str)


def recommend(df, columns, query="", favorite="", count=5):
    data = df.copy()

    if data.empty:
        return data, []

    text_data = data[columns].fillna("").astype(str).agg(
        " ".join, axis=1
    )

    if not query.strip() and not favorite:
        query = "popular trending recommended"

    if favorite:
        selected = data[data["Name"] == favorite]
        if not selected.empty:
            query = (
                query + " " +
                selected.iloc[0][columns].fillna("").astype(str).str.cat(sep=" ")
            )

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )
        matrix = vectorizer.fit_transform(text_data)
        query_vector = vectorizer.transform([query])
        scores = cosine_similarity(query_vector, matrix).flatten()
    except ValueError:
        return data.iloc[0:0].copy(), []

    data["Similarity"] = scores

    if favorite:
        data = data[data["Name"] != favorite]

    data = data[data["Similarity"] > 0]
    data = data.sort_values("Similarity", ascending=False)
    results = data.head(count).copy()

    return results, results["Similarity"].tolist()


def show_results(results, category):
    if results.empty:
        st.warning(
            "No matching recommendations found. "
            "Try changing your filters."
        )
        return

    st.subheader("✨ Recommended for You")
    st.caption(
        "Similarity scores show how closely items match your selections. "
        "They are not model accuracy."
    )

    st.metric("Recommendations Found", len(results))

    for _, item in results.iterrows():
        with st.container(border=True):
            st.markdown(f"### {item['Name']}")

            if category == "Movies":
                c1, c2, c3 = st.columns(3)

                c1.write(f"**Genre:** {item['Genre']}")
                c2.write(f"**Year:** {int(item['Release Year'])}")
                c3.write(f"**IMDb Rating:** {item['IMDb Rating']:.1f}/10")

                c1.write(
                    f"**Trending Score:** {item['Trending Score']}"
                )
                c2.write(
                    f"**Global Views:** "
                    f"{item['Global Views (Millions)']} million"
                )

            elif category == "Books":
                c1, c2, c3 = st.columns(3)

                c1.write(f"**Author:** {item['Author']}")
                c2.write(f"**Genre:** {item['Genre']}")
                c3.write(f"**Rating:** {item['Rating']}/5")

                c1.write(
                    f"**Purchases:** {item['Purchase Count']}"
                )
                c2.write(f"**Stock:** {item['Stock Status']}")

            elif category == "Products":
                c1, c2, c3 = st.columns(3)

                c1.write(f"**Category:** {item['Category']}")
                c2.write(f"**Rating:** {item['Rating']}/5")

                ctr = float(item["Click Through Rate"])
                conversion = float(item["Conversion Rate"])

                if abs(ctr) <= 1:
                    ctr *= 100
                if abs(conversion) <= 1:
                    conversion *= 100

                c3.write(f"**Click-through Rate:** {ctr:.1f}%")
                c1.write(f"**Conversion Rate:** {conversion:.1f}%")

            similarity = float(item["Similarity"])
            st.progress(
                max(0.0, min(1.0, similarity)),
                text=f"Content similarity: {similarity * 100:.1f}%"
            )


if "page" not in st.session_state:
    st.session_state.page = "Home"


if st.session_state.page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>🎯 RecoVerse AI</h1>
        <h3>Your Personal Recommendation System</h3>
        <p>Discover movies, books and products based on your interests.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("## 🎬 Movies")
            st.write("Discover movies based on genre and ratings.")
            st.metric("Movies Available", len(movie_df))
            if st.button("Explore Movies", key="home_movies"):
                st.session_state.page = "Movies"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("## 📚 Books")
            st.write("Find books based on authors and categories.")
            st.metric("Books Available", len(book_df))
            if st.button("Explore Books", key="home_books"):
                st.session_state.page = "Books"
                st.rerun()

    with col3:
        with st.container(border=True):
            st.markdown("## 🛍️ Products")
            st.write("Explore products based on categories and ratings.")
            st.metric("Products Available", len(product_df))
            if st.button("Explore Products", key="home_products"):
                st.session_state.page = "Products"
                st.rerun()

    st.divider()
    st.caption("Developed by Mukul Bandewar")


else:
    category = st.session_state.page

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "Home"
        st.rerun()

    st.title(f"{category} Recommendation System")
    st.write("Choose your preferences and find matching recommendations.")

    if category == "Movies":
        df = movie_df

        genres = sorted(
            df["Genre"].astype(str).unique().tolist()
        )
        selected_genres = st.multiselect(
            "Select Movie Genres",
            genres
        )

        min_rating = float(df["IMDb Rating"].min())
        max_rating = float(df["IMDb Rating"].max())

        if min_rating < max_rating:
            rating_filter = st.slider(
                "Minimum IMDb Rating",
                min_value=min_rating,
                max_value=max_rating,
                value=min_rating,
                step=0.5
            )
        else:
            rating_filter = min_rating

        favorite = st.selectbox(
            "Choose a Movie You Like (Optional)",
            ["None"] + df["Name"].astype(str).tolist()
        )

        count = st.slider(
            "Number of Recommendations",
            min_value=1,
            max_value=min(10, len(df)),
            value=min(5, len(df))
        )

        if st.button("Find Movies"):
            filtered = df.copy()

            if selected_genres:
                filtered = filtered[
                    filtered["Genre"].astype(str).isin(selected_genres)
                ]

            filtered = filtered[
                filtered["IMDb Rating"] >= rating_filter
            ]

            results, _ = recommend(
                filtered,
                ["Name", "Genre", "Description"],
                " ".join(selected_genres),
                "" if favorite == "None" else favorite,
                count
            )

            show_results(results, "Movies")

    elif category == "Books":
        df = book_df

        authors = sorted(
            df["Author"].astype(str).unique().tolist()
        )
        genres = sorted(
            df["Genre"].astype(str).unique().tolist()
        )

        selected_authors = st.multiselect(
            "Select Authors",
            authors
        )
        selected_genres = st.multiselect(
            "Select Book Genres",
            genres
        )

        favorite = st.selectbox(
            "Choose a Book You Like (Optional)",
            ["None"] + df["Name"].astype(str).tolist()
        )

        count = st.slider(
            "Number of Recommendations",
            min_value=1,
            max_value=min(10, len(df)),
            value=min(5, len(df))
        )

        if st.button("Find Books"):
            filtered = df.copy()

            if selected_authors:
                filtered = filtered[
                    filtered["Author"].astype(str).isin(selected_authors)
                ]

            if selected_genres:
                filtered = filtered[
                    filtered["Genre"].astype(str).isin(selected_genres)
                ]

            query = " ".join(selected_authors + selected_genres)

            results, _ = recommend(
                filtered,
                ["Name", "Author", "Genre", "Description"],
                query,
                "" if favorite == "None" else favorite,
                count
            )

            show_results(results, "Books")

    elif category == "Products":
        df = product_df

        categories = sorted(
            df["Category"].astype(str).unique().tolist()
        )
        selected_categories = st.multiselect(
            "Select Product Categories",
            categories
        )

        favorite = st.selectbox(
            "Choose a Product You Like (Optional)",
            ["None"] + df["Name"].astype(str).tolist()
        )

        count = st.slider(
            "Number of Recommendations",
            min_value=1,
            max_value=min(10, len(df)),
            value=min(5, len(df))
        )

        if st.button("Find Products"):
            filtered = df.copy()

            if selected_categories:
                filtered = filtered[
                    filtered["Category"].astype(str).isin(
                        selected_categories
                    )
                ]

            results, _ = recommend(
                filtered,
                ["Name", "Category", "Description"],
                " ".join(selected_categories),
                "" if favorite == "None" else favorite,
                count
            )

            show_results(results, "Products")

    st.divider()
    st.caption("RecoVerse AI | Developed by Mukul Bandewar")
