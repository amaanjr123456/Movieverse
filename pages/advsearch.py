import streamlit as st
import numpy as np
import tensorflow as tf
import time

from pages.nn_model import build_model
from recommender.movie_data import load_movie_data, get_top_movies_per_genre


st.title("✨Do Adv AI Searching")
st.subheader("Select your types")

# Initialising session state
if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = []

# to handle button clicks
def add_genre(genre):
    if genre not in st.session_state.selected_genre:
        st.session_state.selected_genre.append(genre)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📈Adventure + ", key="action1"):
        add_genre("Adventure")
with col2:
    if st.button("🕒Thriller  + ", key="action2"):
        add_genre("Thriller")
with col3:
    if st.button("👊Action    + ", key="action3"):
        add_genre("Action")

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("🎭Drama     + ", key="soft1"):
        add_genre("Drama")
with col5:
    if st.button("😂Comedy    + ", key="soft2"):
        add_genre("Comedy")
with col6:
    if st.button("💝Romance   + ", key="soft3"):
        add_genre("Romance")

col7, col8, col9 = st.columns(3)
with col7:
    if st.button("😮Fantasy   + ", key="social1"):
        add_genre("Fantasy")
with col8:
    if st.button("🔭Sci-Fi    + ", key="social2"):
        add_genre("Sci-Fi")
with col9:
    if st.button("🕵🏻Crime     + ", key="social3"):
        add_genre("Crime")


st.write(st.session_state.selected_genre)

# Genre map
genre_map = {
    "Action": 0, "Drama": 1, "Sci-Fi": 2, "Romance": 3, "Comedy": 4,
    "Adventure": 5, "Thriller": 6, "Fantasy": 7, "Crime": 8
}

def search_ani():
    st.markdown("""
    <style>
    .shimmer-text {
        font-size: 18px;
        font-weight: bold;
        background: linear-gradient(120deg, #ffffff, #aaaaaa, #000000);
        background-size: 200% auto;
        color: transparent;
        background-clip: text;
        -webkit-background-clip: text;
        animation: shimmer 2s linear infinite, fadeOut 1s ease-in-out 3s forwards;
        margin-top: 20px;
    }

    @keyframes shimmer {
        0% {
            background-position: -100% center;
        }
        100% {
            background-position: 200% center;
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
            display: none;
        }
    }
    </style>

    <div class="shimmer-text">🔍 Searching based on genres...</div>
    """, unsafe_allow_html=True)

if st.button("✨Search"):
      selected = st.session_state.selected_genre
      
      if len(selected) != 3:
        st.warning("⚠️ Please select exactly 3 genres.")
      else:
          # small css work👇
        search_ani()  
          
        

        genre_vector = np.zeros((3,))
        for g in selected:
            genre_vector[genre_map[g] % 3] = 1

        input_vector = genre_vector.reshape(1, -1)

        # loading training data
        model = tf.keras.models.load_model("data/movie_model_tf.keras")
        predictions = model.predict(input_vector)[0]

        # Load real movie data
        df = load_movie_data()

        # Collecting top 3 movies per gene
        movie_pool = []
        for g in selected:
            top_movies = get_top_movies_per_genre(df, g, top_n=3)
            movie_pool.extend(top_movies['title'].tolist())

        movie_pool = movie_pool[:9]

        top_indices = np.argsort(predictions)[::-1][:3]
        recommended_movies = [movie_pool[i] for i in top_indices]

        time.sleep(3)
        st.subheader("🍿 Best Recommended Movies for You: ")
        for movie in recommended_movies:
            st.markdown(f"✨ {movie}")
        
        