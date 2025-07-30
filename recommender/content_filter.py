import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_title(title):
    return re.sub(r"\(\d{4}\)", "", title).strip().lower()

movies = pd.read_csv("data/movies.csv")


movies['genres'] = movies['genres'].fillna('').str.split('|')

print([clean_title(title) for title in movies['title'].head(20)])

# One-hot encode genres
genre_dummies = movies['genres'].explode().str.get_dummies().groupby(movies['movieId']).sum()

# the collaborative filtering
genre_similarity = cosine_similarity(genre_dummies)

movie_id_to_title = dict(zip(movies['movieId'], movies['title']))
title_to_movie_id = {clean_title(v): k for k, v in movie_id_to_title.items()}
movie_ids = list(genre_dummies.index)  # ordered list of movieIds

# Recommendation function
def get_recommendations(title, top_n=10):
    title = title.lower()
    if title not in title_to_movie_id:
        return []
    
    movie_id = title_to_movie_id[title]
    if movie_id not in movie_ids:
        return []

    idx = movie_ids.index(movie_id)
    sim_scores = list(enumerate(genre_similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1: top_n + 1]
    
    recommended_ids = [movie_ids[i[0]] for i in sim_scores]
    recommended_titles = [movie_id_to_title[mid] for mid in recommended_ids]
    
    return recommended_titles