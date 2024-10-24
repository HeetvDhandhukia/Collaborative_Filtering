import streamlit as st
import pandas as pd
import os

# Load the Bollywood movies dataset
movies_df = pd.read_csv("BollywoodMovieDetail.csv")

# Predefined genre options
genre_options = ["Action", "Romance", "Horror"]

# CSS for consistent image size
image_style = """
<style>
.poster-container img {
    height: 300px;
    width: 200px;
    object-fit: cover;
    margin: 5px;
    border-radius: 10px;
}
</style>
"""

# Function to recommend movies based on genre
def recommend_movies_by_genre(df, genre, n=5):
    filtered_movies = df[
        df['genre'].str.contains(genre, case=False, na=False) & (df['hitFlop'] >= 3)
    ]
    return filtered_movies['title'].sample(n) if len(filtered_movies) >= n else filtered_movies['title']

# Streamlit UI
st.title("Mood-Based Movie Recommendation System by Genre")
st.markdown(image_style, unsafe_allow_html=True)

selected_genre = st.selectbox("Select a Genre:", genre_options)
num_recommendations = st.slider("Number of Recommendations:", 1, 5, 5)

poster_paths = {
    "Action": ["action.jpg", "action1.jpg", "action2.webp"],
    "Romance": ["romance.jpg", "romance1.jpg", "romance3.jpg"],
    "Horror": ["horror.jpeg", "horror1.jpg"]
}

if st.button("Get Recommendations"):
    recommendations = recommend_movies_by_genre(movies_df, selected_genre, num_recommendations)

    if not recommendations.empty:
        st.subheader(f"{selected_genre} Posters:")
        cols = st.columns(len(poster_paths[selected_genre]))

        for idx, path in enumerate(poster_paths[selected_genre]):
            with cols[idx]:
                if os.path.exists(path):
                    st.image(path, use_column_width=False, width=200)
                else:
                    st.error("Poster not found.")

        st.subheader(f"Top {num_recommendations} Movies for {selected_genre} Genre:")
        for title in recommendations:
            st.write(f"- {title}")
