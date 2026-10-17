
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
}
h1,h2,h3,p,label { color: white; }
.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(120deg,#273c75,#192a56);
    text-align: center;
}
div.stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent

MOVIES_FILE = BASE_DIR / "trending_movies_2026.csv"
BOOKS_FILE = BASE_DIR / "trending_books_2026.csv"
PRODUCTS_FILE = BASE_DIR / "trending_products_2026.csv"


def load_csv(path, required):
    if not path.exists():
        st.error(f"CSV file not found: {path.name}")
        st.stop()

    try:
        data = pd.read_csv(path)
    except Exception as error:
        st.error(f"Could not read {path.name}: {error}")
        st.stop()

    data.columns = data.columns.str.strip()

    missing = set(required) - set(data.columns)
    if missing:
        st.error(
            f"Missing columns in {path.name}: "
            + ", ".join(sorted(missing))
        )
        st.stop()

    if data.empty:
        st.error(f"{path.name} has no records.")
        st.stop()

    return data


def add_price_column(df):
    if "price_usd" in df.columns:
        df["Price (USD)"] = pd.to_numeric(
            df["price_usd"], errors="coerce"
        )
    elif "Price (USD)" in df.columns:
        df["Price (USD)"] = pd.to_numeric(
            df["Price (USD)"], errors="coerce"
        )
    else:
        df["Price (USD)"] = float("nan")

    return df


movie_df = load_csv(MOVIES_FILE, [
    "item_id", "title", "genre", "release_year",
    "average_rating", "trending_score", "global_views_millions"
])

book_df = load_csv(BOOKS_FILE, [
    "item_id", "title", "author", "category",
    "rating", "purchase_count", "stock_status"
])

product_df = load_csv(PRODUCTS_FILE, [
    "item_id", "product_name", "category", "price_usd",
    "rating", "click_through_rate", "conversion_rate"
])

movie_df = movie_df.rename(columns={
    "title": "Name",
    "genre": "Genre",
    "release_year": "Release Year",
    "average_rating": "IMDb Rating",
    "trending_score": "Trending Score",
    "global_views_millions": "Global Views (Millions)"
})

movie_df["IMDb Rating"] = pd.to_numeric(
    movie_df["IMDb Rating"], errors="coerce"
)
movie_df["Trending Score"] = pd.to_numeric(
    movie_df["Trending Score"], errors="coerce"
)
movie_df["Global Views (Millions)"] = pd.to_numeric(
    movie_df["Global Views (Millions)"], errors="coerce"
)
movie_df["Industry"] = "Not specified in CSV"
movie_df["Language"] = "Not specified in CSV"
movie_df["OTT Information"] = "Not provided in CSV"
movie_df["Dubbed Languages"] = "Not provided in CSV"
movie_df["Description"] = movie_df["Genre"].fillna("").astype(str)
movie_df = add_price_column(movie_df)

book_df = book_df.rename(columns={
    "title": "Name",
    "author": "Author",
    "category": "Genre",
    "rating": "Rating",
    "purchase_count": "Purchase Count",
    "stock_status": "Stock Status"
})

book_df["Rating"] = pd.to_numeric(book_df["Rating"], errors="coerce")
book_df["Purchase Count"] = pd.to_numeric(
    book_df["Purchase Count"], errors="coerce"
)
book_df["Description"] = (
    book_df["Genre"].fillna("").astype(str) + " " +
    book_df["Author"].fillna("").astype(str)
)
book_df = add_price_column(book_df)

product_df = product_df.rename(columns={
    "product_name": "Name",
    "category": "Category",
    "price_usd": "Price (USD)",
    "rating": "Rating",
    "click_through_rate": "Click Through Rate",
    "conversion_rate": "Conversion Rate"
})

for column in ["Price (USD)", "Rating", "Click Through Rate", "Conversion Rate"]:
    product_df[column] = pd.to_numeric(
        product_df[column], errors="coerce"
    )

product_df["Description"] = (
    product_df["Category"].fillna("").astype(str)
)

if "usd_inr_rate" not in st.session_state:
    st.session_state.usd_inr_rate = 95.02

with st.sidebar:
    st.header("💱 Currency Settings")

    st.number_input(
        "1 USD = INR",
        min_value=1.0,
        max_value=200.0,
        step=0.10,
        key="usd_inr_rate"
    )

    st.caption(
        "Enter your preferred exchange rate. "
        "This is a manual rate, not a live feed."
    )


def recommend(df, columns, query, favorite, count):
    if df.empty:
        return pd.DataFrame()

    text_data = df[columns].fillna("").astype(str).agg(
        " ".join, axis=1
    )

    if not text_data.str.strip().any():
        return pd.DataFrame()

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        matrix = vectorizer.fit_transform(text_data)
    except ValueError:
        return pd.DataFrame()

    query = str(query).strip()

    if favorite != "None":
        selected_item = df[df["Name"] == favorite]
        if not selected_item.empty:
            query += " " + selected_item.iloc[0][columns].fillna(
                ""
            ).astype(str).str.cat(sep=" ")

    if not query.strip():
        return pd.DataFrame()

    try:
        scores = cosine_similarity(
            vectorizer.transform([query]), matrix
        ).ravel()
    except ValueError:
        return pd.DataFrame()

    results = df.copy()
    results["Similarity"] = scores

    if favorite != "None":
        results = results[results["Name"] != favorite]

    results = results[results["Similarity"] > 0]

    return results.sort_values(
        "Similarity", ascending=False
    ).head(count)


def show_results(results, category):
    if results.empty:
        st.warning(
            "No matching recommendations found. "
            "Try changing your interests or filters."
        )
        return

    st.subheader("✨ Your Recommendations")

    fields = {
        "Movies": [
            "Genre", "Release Year", "IMDb Rating",
            "Trending Score", "Global Views (Millions)"
        ],
        "Books": [
            "Author", "Genre", "Rating",
            "Purchase Count", "Stock Status"
        ],
        "Products": [
            "Category", "Rating",
            "Click Through Rate", "Conversion Rate"
        ]
    }

    rate = st.session_state.usd_inr_rate

    for _, item in results.iterrows():
        with st.container(border=True):
            st.markdown(f"### {item['Name']}")

            price = item.get("Price (USD)", float("nan"))

            if pd.notna(price):
                price = float(price)
                st.write(f"**Price (USD):** ${price:,.2f}")
                st.write(f"**Price (INR):** ₹{price * rate:,.2f}")
            else:
                st.caption(" the CSV.")

            for field in fields[category]:
                value = item.get(field, "")

                if pd.isna(value):
                    continue

                if field == "Global Views (Millions)":
                    value = f"{float(value):,.1f} million"

                elif field in ["IMDb Rating", "Rating"]:
                    value = (
                        f"{value}/10"
                        if category == "Movies"
                        else f"{value}/5"
                    )

                elif field in ["Click Through Rate", "Conversion Rate"]:
                    number = float(value)
                    value = (
                        f"{number * 100:.2f}%"
                        if abs(number) <= 1
                        else f"{number:.2f}%"
                    )

                st.write(f"**{field}:** {value}")

            st.progress(
                min(max(float(item["Similarity"]), 0.0), 1.0),
                text="Content similarity (not accuracy)"
            )


def budget_filter(df, label):
    prices = pd.to_numeric(df["Price (USD)"], errors="coerce")
    available = prices.dropna()

    if available.empty:
        st.info(
            f" is {label}. "
            "budget filtering."
        )
        return df.copy()

    currency = st.radio(
        "Budget currency",
        ["USD ($)", "INR (₹)"],
        horizontal=True,
        key=f"currency_{label}"
    )

    rate = st.session_state.usd_inr_rate
    max_usd = float(available.max())

    if currency == "INR (₹)":
        max_budget = max(100.0, max_usd * rate)
        default_budget = min(30000.0, max_budget)

        budget = st.slider(
            "Maximum budget (₹)",
            0.0, max_budget, default_budget,
            step=max(1.0, min(500.0, max_budget / 100)),
            key=f"budget_inr_{label}"
        )

        budget_usd = budget / rate

    else:
        max_budget = max(1.0, max_usd)
        default_budget = min(500.0, max_budget)

        budget = st.slider(
            "Maximum budget ($)",
            0.0, max_budget, default_budget,
            step=max(0.01, min(25.0, max_budget / 100)),
            key=f"budget_usd_{label}"
        )

        budget_usd = budget

    return df[
        prices.isna() | (prices <= budget_usd)
    ].copy()


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
        (c1, "Movies", "🎬", "Discover trending movies"),
        (c2, "Books", "📚", "Explore books and authors"),
        (c3, "Products", "🛍️", "Find products for your needs")
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

    st.title({
        "Movies": "🎬 Movie Recommendations",
        "Books": "📚 Book Recommendations",
        "Products": "🛍️ Product Recommendations"
    }[category])

    if category == "Movies":
        df = movie_df.copy()

        genres = sorted(set(
            word.strip()
            for value in df["Genre"].dropna()
            for word in str(value).replace("/", " ").split()
            if word.strip()
        ))

        selected = st.multiselect("Movie interests", genres)

        ratings = df["IMDb Rating"].dropna()

        if not ratings.empty:
            rating_min = float(ratings.min())
            rating_max = float(ratings.max())

            if rating_min < rating_max:
                rating = st.slider(
                    "Minimum rating",
                    rating_min, rating_max, rating_min
                )
                df = df[
                    df["IMDb Rating"].isna()
                    | (df["IMDb Rating"] >= rating)
                ]

        favorite = st.selectbox(
            "Favorite movie",
            ["None"] + df["Name"].astype(str).tolist()
        )

        df = budget_filter(df, "Movies")

        count = st.slider(
            "Number of recommendations",
            1, min(10, len(movie_df)), min(5, len(movie_df))
        )

        if selected:
            df = df[df["Genre"].apply(
                lambda value: any(
                    g.lower() in str(value).lower()
                    for g in selected
                )
            )]

        if st.button("✨ Find Movies"):
            show_results(
                recommend(
                    df,
                    ["Name", "Genre", "Description"],
                    " ".join(selected),
                    favorite,
                    count
                ),
                category
            )

        st.info( " Recommendation  "
          
        )

    elif category == "Books":
        df = book_df.copy()

        authors = st.multiselect(
            "Authors (optional)",
            sorted(df["Author"].dropna().unique())
        )

        genres = sorted(set(
            word.strip()
            for value in df["Genre"].dropna()
            for word in str(value).replace("/", " ").split()
            if word.strip()
        ))

        selected = st.multiselect("Book interests", genres)

        favorite = st.selectbox(
            "Favorite book",
            ["None"] + df["Name"].astype(str).tolist()
        )

        df = budget_filter(df, "Books")

        count = st.slider(
            "Number of recommendations",
            1, min(10, len(book_df)), min(5, len(book_df))
        )

        if authors:
            df = df[df["Author"].isin(authors)]

        if selected:
            df = df[df["Genre"].apply(
                lambda value: any(
                    g.lower() in str(value).lower()
                    for g in selected
                )
            )]

        if st.button("✨ Find Books"):
            show_results(
                recommend(
                    df,
                    ["Name", "Author", "Genre", "Description"],
                    " ".join(selected),
                    favorite,
                    count
                ),
                category
            )

    else:
        df = product_df.copy()

        categories = sorted(set(
            word.strip()
            for value in df["Category"].dropna()
            for word in str(value).replace("/", " ").split()
            if word.strip()
        ))

        selected = st.multiselect("Product interests", categories)

        favorite = st.selectbox(
            "Favorite product",
            ["None"] + df["Name"].astype(str).tolist()
        )

        df = budget_filter(df, "Products")

        count = st.slider(
            "Number of recommendations",
            1, min(10, len(product_df)), min(5, len(product_df))
        )

        if selected:
            df = df[df["Category"].apply(
                lambda value: any(
                    g.lower() in str(value).lower()
                    for g in selected
                )
            )]

        if st.button("✨ Find Products"):
            show_results(
                recommend(
                    df,
                    ["Name", "Category", "Description"],
                    " ".join(selected),
                    favorite,
                    count
                ),
                category
            )

st.divider()
st.caption(
    "Developer - Mukul Bandewar | RecoVerse AI | "
    "Python • Streamlit • Pandas"
)
