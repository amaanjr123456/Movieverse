# Streamlit Front End
import streamlit as st
from recommender.content_filter import get_recommendations
from recommender.tmdb_utils import get_poster_url
import pandas as pd
import re
import time

# Title
st.set_page_config(page_title="Movieverse", layout="wide")
st.title("🎬Welcome to Movieverse")
st.markdown("Your smart AI-based movie & series recommender. The more you search, the better it learns.")

# To clearn the title
def clean_title(title):
    return re.sub(r"\(\d{4}\)", "", title).strip().lower()


# Initialise the search history
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# search bar
user_input = st.text_input("🔍 Search for any movie or series", "")

# handling search
if st.button("Search"):
    if user_input:
        st.session_state.search_history.append(user_input)
        st.success(f"Added '{user_input}' to your search history!")

# Current search history
if st.session_state.search_history:
    st.subheader("🔁 History")
    col = st.columns(3)
    st.markdown(st.session_state.search_history)

    # Recommend
    all_recs = []
    for title in st.session_state.search_history:
        clean = clean_title(title)
        recs = get_recommendations(clean)
        all_recs.extend(recs)

    # remove dupli and filter already watched one
    unique_recs = list(set(all_recs) - set(st.session_state.search_history))

    # only top 10
    st.subheader("🎯 You May Also Like these 🔟 Series")
    print("Unique Recs:", unique_recs)
    
    cols = st.columns(2)

    for i, title in enumerate(unique_recs[:10]):
        with cols[i % 2]:
            st.markdown(f"**{i+1}. {title}**")


# A short animation using CSS
def show_transition_animation():
    st.markdown("""
    <style>
    /* Fullscreen Overlay */
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #0f0f0f, #1f1f1f);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }

    /* Text Styling */
    .overlay-text {
        color: white;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        animation: glow 2s ease-in-out infinite alternate;
    }

    /* Pulsing icon (✨) */
    .gear {
        display: inline-block;
        font-size: 48px;
        margin-bottom: 20px;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    @keyframes glow {
        from { text-shadow: 0 0 10px #ffff33; }
        to { text-shadow: 0 0 30px #ffd700; }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    </style>

    <div class="overlay">
        <div class="overlay-text">
            <div class="gear">✨</div><br>
            Entering Advanced Search Mode...
        </div>
    </div>
""", unsafe_allow_html=True)

if st.button("Lets Go Adv✨"):
    show_transition_animation()
    time.sleep(3)
    st.switch_page("pages/advsearch.py")
