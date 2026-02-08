# backend/collaborative_engine.py
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# Paths
DATA_PATH = "data"
MODEL_PATH = "models"

def load_data():
    print("⏳ Loading MovieLens data...")
    ratings = pd.read_csv(os.path.join(DATA_PATH, "ratings.csv"))
    movies = pd.read_csv(os.path.join(DATA_PATH, "movies_small.csv")) # Renamed from movies.csv
    
    # Merge to get titles
    df = pd.merge(ratings, movies, on='movieId')
    return df

def build_collaborative_model():
    df = load_data()
    
    print("🧹 Cleaning data...")
    # 1. Filter out rarely rated movies (Noise reduction)
    # We only want movies that have been rated at least 50 times
    movie_stats = df.groupby('title').agg({'rating': [np.size, np.mean]})
    popular_movies = movie_stats['rating']['size'] >= 50
    df_filtered = df[df['title'].isin(movie_stats[popular_movies].index)]

    # 2. Create User-Item Matrix (Pivot Table)
    # Rows: User IDs, Cols: Movie Titles, Values: Ratings
    print("📊 Creating User-Item Matrix...")
    user_movie_matrix = df_filtered.pivot_table(index='userId', columns='title', values='rating')
    
    # Fill NaN with 0 (unrated)
    # Note: For advanced SVD, we might normalize this, but 0 works for basic SVD
    user_movie_matrix_filled = user_movie_matrix.fillna(0)

    # 3. Apply SVD (Dimensionality Reduction)
    # We compress the user-movie matrix into 12 latent components (features)
    print("🧮 Training SVD Model...")
    X = user_movie_matrix_filled.values.T # Transpose: We want Item-Item similarity
    
    SVD = TruncatedSVD(n_components=12, random_state=42)
    matrix_reduced = SVD.fit_transform(X)
    
    # 4. Calculate Correlation Matrix
    # This tells us how similar every movie is to every other movie based on USER RATINGS
    corr_mat = np.corrcoef(matrix_reduced)
    
    # 5. Save Models
    print("💾 Saving collaborative models...")
    pickle.dump(corr_mat, open(os.path.join(MODEL_PATH, 'collab_similarity.pkl'), 'wb'))
    pickle.dump(user_movie_matrix.columns, open(os.path.join(MODEL_PATH, 'collab_titles.pkl'), 'wb'))
    
    print("✅ Collaborative Model Built!")
    return user_movie_matrix, corr_mat

def recommend_collaborative(movie_title):
    # Load data
    try:
        corr_mat = pickle.load(open(os.path.join(MODEL_PATH, 'collab_similarity.pkl'), 'rb'))
        titles = pickle.load(open(os.path.join(MODEL_PATH, 'collab_titles.pkl'), 'rb'))
    except FileNotFoundError:
        print("❌ Models not found. Run build_collaborative_model() first.")
        return []

    title_list = list(titles)
    
    if movie_title not in title_list:
        return [f"Movie '{movie_title}' not found in collaborative dataset."]
    
    # Find index of the movie
    idx = title_list.index(movie_title)
    
    # Get correlation vector for this movie
    corr_movie = corr_mat[idx]
    
    # Find movies with high correlation (>0.9)
    # This logic finds movies that user rating patterns suggest are similar
    recommendations = []
    
    # Sort by correlation score (descending)
    sorted_indices = np.argsort(corr_movie)[::-1]
    
    # Get top 10 (excluding the movie itself)
    for i in sorted_indices[1:11]: 
        recommendations.append(title_list[i])
        
    return recommendations

if __name__ == "__main__":
    # 1. Build the model (Uncomment to run once)
    build_collaborative_model()
    
    # 2. Test
    test_movie = "Toy Story (1995)"
    print(f"\n👥 Users who liked '{test_movie}' also liked:")
    recs = recommend_collaborative(test_movie)
    print(recs)