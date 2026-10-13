
import streamlit as st
import pandas as pd
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
    background: linear-gradient(135deg, #0b1220, #172943);
    color: #ffffff;
}
h1, h2, h3, p, label {
    color: white;
}
.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(120deg, #273c75, #192a56);
    text-align: center;
}
.small-note {
    color: #b9c7dc;
    font-size: 13px;
}
div.stButton > button {
    width: 100%;
    min-height: 45px;
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


movies = [
    ("3 Idiots", "Indian", "Comedy Drama", "Hindi",
     8.4, "Prime Video / regional availability varies",
     "Hindi, Tamil (verify dub)", "College, friendship, engineering"),

    ("Dangal", "Indian", "Sports Drama", "Hindi",
     8.3, "Netflix / regional availability varies",
     "Hindi, Tamil, Telugu (verify)", "Wrestling, family, motivation"),

    ("Lagaan", "Indian", "Sports Drama", "Hindi",
     8.1, "Check current OTT catalogue",
     "Hindi", "Cricket, village, history"),

    ("Taare Zameen Par", "Indian", "Drama Family", "Hindi",
     8.3, "Check current OTT catalogue",
     "Hindi", "Education, children, emotions"),

    ("Zindagi Na Milegi Dobara", "Indian", "Adventure Drama", "Hindi",
     8.2, "Check current OTT catalogue",
     "Hindi", "Travel, friendship, life"),

    ("Drishyam", "Indian", "Crime Thriller", "Hindi",
     8.2, "Check current OTT catalogue",
     "Hindi", "Mystery, investigation, family"),

    ("Andhadhun", "Indian", "Crime Thriller", "Hindi",
     8.2, "Check current OTT catalogue",
     "Hindi", "Mystery, crime, suspense"),

    ("12th Fail", "Indian", "Drama Motivation", "Hindi",
     8.8, "Check current OTT catalogue",
     "Hindi", "Education, UPSC, determination"),

    ("Jawan", "Indian", "Action Thriller", "Hindi",
     6.9, "Netflix / regional availability varies",
     "Hindi, Tamil, Telugu (verify)", "Action, revenge, justice"),

    ("RRR", "Indian", "Action Drama", "Telugu",
     7.8, "Netflix / regional availability varies",
     "Telugu, Hindi, Tamil, Kannada, Malayalam",
     "Action, friendship, history"),

    ("Kantara", "Indian", "Action Thriller", "Kannada",
     8.2, "Check current OTT catalogue",
     "Kannada, Hindi, Tamil, Telugu (verify)",
     "Folklore, mystery, action"),

    ("Baahubali 2", "Indian", "Action Fantasy", "Telugu",
     8.2, "Check current OTT catalogue",
     "Telugu, Hindi, Tamil, Malayalam (verify)",
     "Fantasy, kingdom, war"),

    ("3 Idiots", "Indian", "Comedy Drama", "Hindi",
     8.4, "Prime Video / regional availability varies",
     "Hindi", "Engineering, college, friendship"),

    ("Queen", "Indian", "Comedy Drama", "Hindi",
     8.1, "Check current OTT catalogue",
     "Hindi", "Travel, independence, self-discovery"),

    ("Chak De India", "Indian", "Sports Drama", "Hindi",
     8.1, "Check current OTT catalogue",
     "Hindi", "Hockey, teamwork, sports"),

    ("Interstellar", "Hollywood", "Sci-Fi Adventure", "English",
     8.7, "Check current OTT catalogue",
     "English; dubbed versions vary by platform",
     "Space, science, survival"),

    ("Inception", "Hollywood", "Sci-Fi Thriller", "English",
     8.8, "Check current OTT catalogue",
     "English; dubbed versions vary by platform",
     "Dreams, mind, science fiction"),

    ("The Dark Knight", "Hollywood", "Action Crime", "English",
     9.0, "Check current OTT catalogue",
     "English; dubbed versions vary by platform",
     "Batman, crime, justice"),

    ("The Matrix", "Hollywood", "Sci-Fi Action", "English",
     8.7, "Check current OTT catalogue",
     "English; dubbed versions vary by platform",
     "Artificial intelligence, reality, action"),

    ("Avengers Endgame", "Hollywood", "Action Sci-Fi", "English",
     8.4, "Check current OTT catalogue",
     "English; Hindi and other dubs may be available",
     "Superheroes, action, universe"),

    ("The Shawshank Redemption", "Hollywood", "Drama", "English",
     9.3, "Check current OTT catalogue",
     "English; check regional audio options",
     "Prison, hope, friendship"),

    ("Titanic", "Hollywood", "Romance Drama", "English",
     7.9, "Check current OTT catalogue",
     "English; check regional audio options",
     "Romance, ship, history"),

    ("The Conjuring", "Hollywood", "Horror Mystery", "English",
     7.5, "Check current OTT catalogue",
     "English; check regional audio options",
     "Horror, ghosts, supernatural"),

    ("The Martian", "Hollywood", "Sci-Fi Adventure", "English",
     8.0, "Check current OTT catalogue",
     "English; check regional audio options",
     "Mars, survival, science"),

    ("Joker", "Hollywood", "Crime Drama", "English",
     8.3, "Check current OTT catalogue",
     "English; check regional audio options",
     "Psychology, crime, society"),

    ("Jurassic Park", "Hollywood", "Adventure Sci-Fi", "English",
     8.2, "Check current OTT catalogue",
     "English; check regional audio options",
     "Dinosaurs, science, adventure"),
]

books = [
    ("Atomic Habits", "James Clear", "Self Help Productivity",
     "Habits, discipline, personal growth"),
    ("The Psychology of Money", "Morgan Housel", "Finance Psychology",
     "Money, investing, financial behaviour"),
    ("Rich Dad Poor Dad", "Robert Kiyosaki", "Finance Business",
     "Money, assets, financial education"),
    ("Ikigai", "Hector Garcia", "Self Help Philosophy",
     "Purpose, happiness, Japanese lifestyle"),
    ("Deep Work", "Cal Newport", "Productivity Education",
     "Focus, concentration, deep learning"),
    ("Wings of Fire", "A. P. J. Abdul Kalam", "Biography Motivation",
     "Science, India, determination"),
    ("The Alchemist", "Paulo Coelho", "Fiction Adventure",
     "Dreams, journey, self discovery"),
    ("Harry Potter", "J. K. Rowling", "Fantasy Adventure",
     "Magic, friendship, wizard school"),
    ("Think and Grow Rich", "Napoleon Hill", "Business Motivation",
     "Success, mindset, goals"),
    ("The Hobbit", "J. R. R. Tolkien", "Fantasy Adventure",
     "Dragons, quests, fantasy"),
    ("1984", "George Orwell", "Fiction Thriller",
     "Dystopia, government, surveillance"),
    ("To Kill a Mockingbird", "Harper Lee", "Fiction Drama",
     "Justice, society, morality"),
    ("Sapiens", "Yuval Noah Harari", "History Science",
     "Human history, civilization, evolution"),
    ("The Discovery of India", "Jawaharlal Nehru", "History India",
     "Indian history, culture, civilization"),
    ("The Guide", "R. K. Narayan", "Fiction Drama",
     "Indian life, relationships, transformation"),
    ("Clean Code", "Robert C. Martin", "Programming Education",
     "Software development, coding, best practices"),
    ("Learning Python", "Mark Lutz", "Programming Education",
     "Python, programming, software"),
    ("Introduction to Algorithms", "Cormen et al.",
     "Programming Computer Science",
     "Algorithms, data structures, computer science"),
    ("The Intelligent Investor", "Benjamin Graham",
     "Finance Business", "Investing, markets, financial strategy"),
    ("Man's Search for Meaning", "Viktor Frankl",
     "Psychology Philosophy", "Meaning, resilience, purpose"),
]

products = [
    ("Gaming Laptop", "Electronics Gaming",
     "Gaming, coding, powerful processor", 65000),
    ("Student Laptop", "Electronics Education",
     "Study, coding, college, productivity", 40000),
    ("Wireless Headphones", "Electronics Music",
     "Music, wireless audio, travel", 2500),
    ("Bluetooth Speaker", "Electronics Music",
     "Music, portable audio, entertainment", 1800),
    ("Smart Watch", "Electronics Fitness",
     "Fitness, notifications, health tracking", 3000),
    ("Mechanical Keyboard", "Electronics Gaming",
     "Typing, gaming, programming", 3500),
    ("Wireless Mouse", "Electronics Computer",
     "Office, laptop, productivity", 800),
    ("Running Shoes", "Sports Fitness",
     "Running, walking, exercise", 2200),
    ("Yoga Mat", "Fitness Wellness",
     "Yoga, exercise, stretching", 700),
    ("Digital Camera", "Electronics Photography",
     "Photography, travel, video", 45000),
    ("Travel Backpack", "Travel Accessories",
     "Travel, college, luggage", 1500),
    ("Python Programming Book", "Education Programming",
     "Python, coding, learning", 600),
    ("Drawing Tablet", "Electronics Art",
     "Digital art, design, drawing", 5000),
    ("Power Bank", "Electronics Accessories",
     "Charging, smartphone, travel", 1200),
    ("External SSD", "Electronics Computer",
     "Storage, backups, fast file transfer", 5000),
    ("Fitness Resistance Bands", "Sports Fitness",
     "Home workout, strength, exercise", 500),
    ("Office Chair", "Furniture Productivity",
     "Office, comfort, working from home", 7000),
    ("Tablet", "Electronics Education",
     "Reading, studying, video, productivity", 18000),
    ("Smartphone", "Electronics Mobile",
     "Photography, communication, apps", 20000),
    ("E-Reader", "Electronics Books",
     "Reading, ebooks, portable library", 12000),
]

movie_df = pd.DataFrame(
    movies,
    columns=[
        "Name", "Industry", "Genre", "Language",
        "IMDb Rating", "OTT Information",
        "Dubbed Languages", "Description"
    ]
)

book_df = pd.DataFrame(
    books,
    columns=["Name", "Author", "Genre", "Description"]
)

product_df = pd.DataFrame(
    products,
    columns=["Name", "Category", "Description", "Price (INR)"]
)

def recommend(df, text_columns, preference, selected_name, count):
    df = df.copy()

    if not preference.strip() and selected_name == "None":
        return pd.DataFrame()

    combined = df[text_columns].fillna("").astype(str).agg(
        " ".join, axis=1
    )

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )
    item_matrix = vectorizer.fit_transform(combined)

    query = preference

    if selected_name != "None":
        matching = df[df["Name"] == selected_name]
        if not matching.empty:
            query += " " + matching.iloc[0][text_columns].fillna(
                ""
            ).astype(str).str.cat(sep=" ")

    if not query.strip():
        return pd.DataFrame()

    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, item_matrix).ravel()

    df["Similarity"] = scores

    if selected_name != "None":
        df = df[df["Name"] != selected_name]

    return df.sort_values(
        "Similarity", ascending=False
    ).head(count)

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
    st.write("Choose a category to start your personalized experience.")

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.markdown("## 🎬 Movies")
            st.write("Indian cinema and Hollywood")
            st.write("IMDb ratings, genres, OTT and language information")
            if st.button("Explore Movies", key="home_movies"):
                st.session_state.page = "Movies"
                st.rerun()

    with c2:
        with st.container(border=True):
            st.markdown("## 📚 Books")
            st.write("Indian and international authors")
            st.write("Fiction, technology, finance and self-help")
            if st.button("Explore Books", key="home_books"):
                st.session_state.page = "Books"
                st.rerun()

    with c3:
        with st.container(border=True):
            st.markdown("## 🛍️ Products")
            st.write("Technology, education, fitness and more")
            st.write("Find items matching your budget and interests")
            if st.button("Explore Products", key="home_products"):
                st.session_state.page = "Products"
                st.rerun()

    st.divider()
    st.caption(
        "Recommendations use content similarity. "
        "This demo does not guarantee recommendation accuracy."
    )


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
        df = movie_df

        col1, col2 = st.columns(2)

        with col1:
            industry = st.selectbox(
                "Cinema",
                ["All", "Indian", "Hollywood"]
            )

            available_genres = sorted(set(
                genre
                for item in df["Genre"]
                for genre in item.split()
            ))

            genres = st.multiselect(
                "Genres",
                available_genres
            )

            language = st.multiselect(
                "Original language",
                sorted(df["Language"].unique())
            )

        with col2:
            min_rating = st.slider(
                "Minimum IMDb rating (approximate sample data)",
                0.0, 10.0, 0.0, 0.5
            )

            dubbed = st.selectbox(
                "Dubbed-language preference",
                ["Any", "Hindi", "Tamil", "Telugu",
                 "Kannada", "Malayalam", "English"]
            )

            favorite = st.selectbox(
                "A movie you already like",
                ["None"] + df["Name"].tolist()
            )

        query = " ".join(genres + ([dubbed] if dubbed != "Any" else []))

        filtered = df.copy()

        if industry != "All":
            filtered = filtered[filtered["Industry"] == industry]

        if language:
            filtered = filtered[filtered["Language"].isin(language)]

        filtered = filtered[filtered["IMDb Rating"] >= min_rating]

        if genres:
            filtered = filtered[
                filtered["Genre"].apply(
                    lambda x: any(g in x.split() for g in genres)
                )
            ]

        if dubbed != "Any":
            filtered = filtered[
                filtered["Dubbed Languages"].str.contains(
                    dubbed, case=False, na=False
                )
            ]

        count = st.slider("Number of recommendations", 3, 10, 5)

        if st.button("✨ Find Movies"):
            if filtered.empty:
                st.warning("No titles match all selected filters.")
            else:
                results = recommend(
                    filtered,
                    ["Genre", "Description", "Language",
                     "Industry", "Dubbed Languages"],
                    query,
                    favorite,
                    count
                )

                if results.empty:
                    st.info("Choose a genre or favorite movie.")
                else:
                    st.subheader("Your Recommendations")

                    for _, item in results.iterrows():
                        with st.container(border=True):
                            st.markdown(f"### 🎥 {item['Name']}")
                            st.write(
                                f"**Industry:** {item['Industry']} | "
                                f"**Genre:** {item['Genre']}"
                            )
                            st.write(
                                f"**Original language:** {item['Language']}"
                            )
                            st.write(
                                f"**IMDb rating (approx.):** "
                                f"{item['IMDb Rating']}/10"
                            )
                            st.write(
                                f"**OTT:** {item['OTT Information']}"
                            )
                            st.write(
                                f"**Dubbed languages:** "
                                f"{item['Dubbed Languages']}"
                            )
                            st.write(item["Description"])
                            st.progress(
                                float(item["Similarity"]),
                                text="Content similarity (not accuracy)"
                            )

        st.info(
            "OTT and dubbed-audio information is indicative and may be "
            "outdated. Verify the title on the platform in your region. "
            "IMDb ratings are approximate sample values, not live data."
        )

    elif category == "Books":
        df = book_df

        authors = st.multiselect(
            "Authors (optional)",
            sorted(df["Author"].unique())
        )

        genres = sorted(set(
            genre for value in df["Genre"] for genre in value.split()
        ))

        selected_genres = st.multiselect("Book interests", genres)

        favorite = st.selectbox(
            "A book you like",
            ["None"] + df["Name"].tolist()
        )

        count = st.slider("Number of recommendations", 3, 10, 5)

        if st.button("✨ Find Books"):
            filtered = df.copy()

            if authors:
                filtered = filtered[filtered["Author"].isin(authors)]

            if selected_genres:
                filtered = filtered[
                    filtered["Genre"].apply(
                        lambda x: any(
                            g in x.split() for g in selected_genres
                        )
                    )
                ]

            results = recommend(
                filtered,
                ["Name", "Author", "Genre", "Description"],
                " ".join(selected_genres),
                favorite,
                count
            )

            if results.empty:
                st.warning("Choose a genre or favorite book.")
            else:
                for _, item in results.iterrows():
                    with st.container(border=True):
                        st.markdown(f"### 📚 {item['Name']}")
                        st.write(f"**Author:** {item['Author']}")
                        st.write(f"**Genres:** {item['Genre']}")
                        st.write(item["Description"])
                        st.progress(
                            float(item["Similarity"]),
                            text="Content similarity (not accuracy)"
                        )

    else:
        df = product_df

        categories = sorted(set(
            category_name
            for value in df["Category"]
            for category_name in value.split()
        ))

        selected_categories = st.multiselect(
            "Product interests", categories
        )

        budget = st.slider(
            "Maximum budget (₹)",
            min_value=500,
            max_value=100000,
            value=30000,
            step=500
        )

        favorite = st.selectbox(
            "A product you like",
            ["None"] + df["Name"].tolist()
        )

        count = st.slider("Number of recommendations", 3, 10, 5)

        if st.button("✨ Find Products"):
            filtered = df[df["Price (INR)"] <= budget].copy()

            if selected_categories:
                filtered = filtered[
                    filtered["Category"].apply(
                        lambda x: any(
                            c in x.split() for c in selected_categories
                        )
                    )
                ]

            results = recommend(
                filtered,
                ["Name", "Category", "Description"],
                " ".join(selected_categories),
                favorite,
                count
            )

            if results.empty:
                st.warning("No products match your filters and budget.")
            else:
                for _, item in results.iterrows():
                    with st.container(border=True):
                        st.markdown(f"### 🛍️ {item['Name']}")
                        st.write(f"**Category:** {item['Category']}")
                        st.write(f"**Sample price:** ₹{item['Price (INR)']:,}")
                        st.write(item["Description"])
                        st.progress(
                            float(item["Similarity"]),
                            text="Content similarity (not accuracy)"
                        )

st.divider()
st.caption(
    "RecoVerse AI | Python • Streamlit • TF-IDF • Cosine Similarity"
)

