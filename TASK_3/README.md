# RecoVerse AI – Personal Recommendation Hub

## About the Project

RecoVerse AI is a Python-based recommendation system that helps users discover movies, books, and products according to their interests.

I developed this project using Streamlit and machine learning techniques to make the recommendation process simple and interactive. Users can select their favorite items, apply filters, and get suggestions based on content similarity.

## Features

- **Movie Recommendations:** Find movies based on genre, industry, language, and rating.
- **Book Recommendations:** Explore books based on authors and interests.
- **Product Recommendations:** Discover products according to categories and budget.
- **Favorite Items:** Select a movie, book, or product to find similar options.
- **Interactive Interface:** Simple design with separate sections for each category.
- **Content-Based Filtering:** Uses TF-IDF and Cosine Similarity to compare items.

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity

## How It Works

The application stores a small dataset of movies, books, and products. When users select their preferences or a favorite item, the system compares the available text information.

TF-IDF converts text into numerical vectors, and Cosine Similarity measures how closely the items match the selected preferences. The application then displays the most similar items as recommendations.

## Project Structure

```text
RecoVerse-AI/
├── app.py
├── requirements.txt
└── README.md
```

- `app.py` contains the main application and recommendation logic.
- `requirements.txt` contains the required Python libraries.
- `README.md` contains project information and setup instructions.

## Installation and Setup

**Step 1: Clone the repository**

```bash
git clone https://github.com/your-username/RecoVerse-AI.git
```

**Step 2: Open the project folder**

```bash
cd RecoVerse-AI
```

**Step 3: Install the required libraries**

```bash
pip install -r requirements.txt
```

**Step 4: Start the application**

```bash
streamlit run app.py
```

The application will open in your web browser.

## Requirements

Add these libraries to your `requirements.txt` file:

```text
streamlit
pandas
scikit-learn
```

## What I Learned

While working on this project, I learned how to build an interactive web application using Streamlit and manage datasets with Pandas. I also gained practical knowledge of TF-IDF vectorization and Cosine Similarity and how these techniques can be used to build a basic recommendation system.

## Future Improvements

- Add more movies, books, and products.
- Include posters, book covers, and product images.
- Connect the application to external APIs for updated information.
- Add user accounts and save favorite items.
- Improve recommendations using user ratings and feedback.

## Conclusion

RecoVerse AI is a small project that demonstrates how machine learning techniques can help users discover movies, books, and products based on their interests. It combines text similarity with an easy-to-use interface to provide a simple recommendation experience.

**Project developed using Python, Streamlit, Pandas, and Scikit-learn.**
