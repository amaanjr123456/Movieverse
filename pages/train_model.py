import numpy as np
from nn_model import build_model
from recommender.movie_data import load_movie_data, create_training_data

def train_model():
    genre_map = {
        "Action": 0, "Drama": 1, "Sci-Fi": 2, "Romance": 3, "Comedy": 4,
        "Adventure": 5, "Thriller": 6, "Fantasy": 7, "Crime": 8
    }

    print("📥 Loading and processing movie data...")
    merged_df = load_movie_data()

    print("🧪 Creating training data from genres and top-rated movies...")
    X, y = create_training_data(merged_df, genre_map)

    print(f"🔢 Training samples: {len(X)}, Feature Shape: {X.shape}, Labels shape: {y.shape}")
    model = build_model()

    print("🚀 Training the model...")
    model.fit(X, y, epochs=50, verbose=1)

    model.save("data/movie_model_tf.keras")
    print("✅ Model trained and saved to data/movie_model_tf.keras")

if __name__ == "__main__":
    train_model()