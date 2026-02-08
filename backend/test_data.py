# backend/test_data.py
import pandas as pd
import os

# Define paths
DATA_PATH = "data"

def load_data():
    try:
        # Load TMDB Data
        movies = pd.read_csv(os.path.join(DATA_PATH, "tmdb_5000_movies.csv"))
        credits = pd.read_csv(os.path.join(DATA_PATH, "tmdb_5000_credits.csv"))
        
        # Load MovieLens Data
        ratings = pd.read_csv(os.path.join(DATA_PATH, "ratings.csv"))
        
        print("✅ Data Loaded Successfully!")
        print(f"Movies Shape: {movies.shape}")
        print(f"Credits Shape: {credits.shape}")
        print(f"Ratings Shape: {ratings.shape}")
        
        print("\n--- Sample Movie Data ---")
        print(movies[['title', 'overview']].head(2))
        
        return movies, credits, ratings
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure you downloaded the files and placed them in the 'backend/data' folder.")

if __name__ == "__main__":
    load_data()