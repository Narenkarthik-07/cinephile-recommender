# backend/preprocessing.py
import pandas as pd
import ast # Abstract Syntax Tree - to evaluate strings as Python objects

def load_and_clean_data():
    print("⏳ Loading data...")
    movies = pd.read_csv('data/tmdb_5000_movies.csv')
    credits = pd.read_csv('data/tmdb_5000_credits.csv')

    # Merge datasets on 'title'
    # The movies dataset has the plot/genres, credits has the actors/director
    movies = movies.merge(credits, on='title')

    # Select only the columns we need
    # 'id_x' is the TMDB ID (we keep it for poster fetching later)
    movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    
    # Drop movies with missing overview (rare, but happens)
    movies.dropna(inplace=True)

    return movies

# --- Helper Functions for Text Extraction ---

def convert(text):
    """Parses JSON string and returns a list of 'name' values."""
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

def convert3(text):
    """Extracts the top 3 actors."""
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            L.append(i['name'])
            counter += 1
    return L

def fetch_director(text):
    """Finds the crew member where job is 'Director'."""
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break # Only take the first director found
    return L

def collapse(L):
    """
    Removes spaces from names (e.g., 'Sam Worthington' -> 'SamWorthington').
    This is CRITICAL so the vectorizer treats 'SamWorthington' as a unique entity,
    distinct from 'Sam Mendes'.
    """
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1

# --- Main Processing ---

def prepare_data(movies):
    print("🛠 Processing features...")
    
    # Apply parsing functions
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert3)
    movies['crew'] = movies['crew'].apply(fetch_director)
    
    # Apply space removal for better tokenization
    movies['cast'] = movies['cast'].apply(collapse)
    movies['crew'] = movies['crew'].apply(collapse)
    movies['genres'] = movies['genres'].apply(collapse)
    movies['keywords'] = movies['keywords'].apply(collapse)
    
    # Split overview into list of words
    movies['overview'] = movies['overview'].apply(lambda x: x.split())

    # Create the 'tags' column (The "Soup")
    # We combine Overview + Genres + Keywords + Cast + Director
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    # Join list back to string
    new_df = movies[['movie_id', 'title', 'tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    
    # Lowercase everything for consistency
    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
    
    print("✅ Data Preparation Complete!")
    return new_df

if __name__ == "__main__":
    # Test run
    raw_movies = load_and_clean_data()
    final_df = prepare_data(raw_movies)
    print(final_df.head())