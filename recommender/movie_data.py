import pandas as pd
import numpy as np

def load_movie_data():
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")

    avg_ratings = ratings.groupby("movieId")['rating'].mean().reset_index()
    avg_ratings.rename(columns={"rating": "avg_rating"}, inplace=True)

    # Merge avg ratings into movies
    merged_df = pd.merge(movies, avg_ratings, on="movieId")

    # Split genres into list for each movie
    merged_df['genres'] = merged_df['genres'].apply(lambda x: x.split('|'))

    # Explode into multiple rows per genre for genre-wise filtering
    merged_df = merged_df.explode('genres')

    return merged_df

def get_top_movies_per_genre(df, genre, top_n=3):
    genre_movies = df[df['genres'].str.contains(genre, case=False, na=False)]
    top_movies = genre_movies.sort_values(by='avg_rating', ascending=False).head(top_n)
    return top_movies[['title', 'genres', 'avg_rating']]

# Preparing training data for NN (X = genre_vector, y = one-hot output for top 3 movie)
def create_training_data(merged_df, genre_map):
    X = []
    y = []

    for genre, index in genre_map.items():
        genre_df = merged_df[merged_df['genres'].astype(str).str.lower() == genre.lower()]
        top_movies = (
            genre_df.groupby('movieId').agg({'avg_rating': 'mean', 'title': 'first'}).sort_values('avg_rating', ascending=False).head(3)
        )

        if len(top_movies) < 3:
            continue

        for i, (movie_id, row) in enumerate(top_movies.iterrows()):
            genre_vector = np.zeros(len(genre_map))
            genre_vector[index % 3] = 1

            label = np.zeros(3)
            label[i] = 1 #one hot encode output

            X.append(genre_vector)
            y.append(label)

    return np.array(X), np.array(y)