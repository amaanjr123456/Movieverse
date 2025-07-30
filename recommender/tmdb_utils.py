import requests
import os
from dotenv import load_dotenv

#Loading the API key
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def get_poster_url(movie_title):
    return None
    """url = "http://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None
    
    data = response.json()
    results = data.get("results")
    if not results:
        return None
    
    poster_path = results[0].get("poster_path")
    if not poster_path:
        return None

    full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_url"""