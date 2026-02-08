# backend/content_engine.py
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import load_and_clean_data, prepare_data
import os

# Define paths to save models
MODEL_PATH = "models"
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

def build_content_model():
    # 1. Get Data
    raw_movies = load_and_clean_data()
    final_df = prepare_data(raw_movies)

    # 2. Vectorization
    # max_features=5000: Keep only top 5000 most frequent words to save memory
    # stop_words='english': Remove common words like 'the', 'and', 'is'
    print("🧮 Vectorizing data...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(final_df['tags']).toarray()

    # 3. Similarity Calculation
    # This creates a 4806x4806 matrix containing the similarity score 
    # of every movie against every other movie.
    print("📐 Calculating Cosine Similarity...")
    similarity = cosine_similarity(vectors)

    # 4. Save to disk (Pickle)
    # We save the dataframe (for movie titles/IDs) and the similarity matrix
    print("💾 Saving models...")
    pickle.dump(final_df, open(os.path.join(MODEL_PATH, 'movie_list.pkl'), 'wb'))
    pickle.dump(similarity, open(os.path.join(MODEL_PATH, 'similarity.pkl'), 'wb'))
    
    print("✅ Content-Based Model Built & Saved!")

def recommend(movie_title):
    # Load data
    movies = pickle.load(open(os.path.join(MODEL_PATH, 'movie_list.pkl'), 'rb'))
    similarity = pickle.load(open(os.path.join(MODEL_PATH, 'similarity.pkl'), 'rb'))
    
    # Check if movie exists
    if movie_title not in movies['title'].values:
        return [f"Movie '{movie_title}' not found."]

    # Find the index of the movie in the dataframe
    movie_index = movies[movies['title'] == movie_title].index[0]
    
    # Get similarity scores for this movie
    distances = similarity[movie_index]
    
    # Sort closest movies (exclude the movie itself at index 0)
    # enumerate helps keep track of original index (movie_id)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommendations = []
    for i in movies_list:
        recommendations.append(movies.iloc[i[0]].title)
        
    return recommendations

if __name__ == "__main__":
    # Uncomment this line to build the model for the first time:
    build_content_model()
    
    # Test Recommendation
    print("\n🎥 Testing Recommendation for 'Batman Begins':")
    print(recommend('Batman Begins'))