# backend/hybrid_engine.py
import pandas as pd
import pickle
import os
import re

# Paths
MODEL_PATH = "models"

def clean_title(title):
    """
    Removes year from title, e.g., 'Toy Story (1995)' -> 'toy story'
    Removes trailing spaces and lowercases for better matching.
    """
    return re.sub(r'\s*\(\d{4}\)', '', title).strip().lower()

def get_hybrid_recommendations(movie_title, top_n=10):
    # 1. Load Models
    try:
        # Content Models
        movies_content = pickle.load(open(os.path.join(MODEL_PATH, 'movie_list.pkl'), 'rb'))
        similarity_content = pickle.load(open(os.path.join(MODEL_PATH, 'similarity.pkl'), 'rb'))
        
        # Collaborative Models
        similarity_collab = pickle.load(open(os.path.join(MODEL_PATH, 'collab_similarity.pkl'), 'rb'))
        titles_collab = pickle.load(open(os.path.join(MODEL_PATH, 'collab_titles.pkl'), 'rb'))
    except FileNotFoundError:
        return ["Error: Models not found. Please run previous phases first."]

    # 2. Check if movie exists in Content DB (Primary DB)
    # We use the raw title here
    matches = movies_content[movies_content['title'].str.lower() == movie_title.lower()]
    if matches.empty:
        return [f"Movie '{movie_title}' not found in Content Database."]
    
    movie_idx_content = matches.index[0]
    
    # 3. Get Content-Based Scores
    # We get ALL scores, not just top 10, so we can mix them later
    content_scores = list(enumerate(similarity_content[movie_idx_content]))
    
    # Create a DataFrame for Content Scores
    content_data = []
    for i, score in content_scores:
        title = movies_content.iloc[i]['title']
        content_data.append({'title': title, 'content_score': score})
    df_content = pd.DataFrame(content_data)

    # 4. Get Collaborative Scores
    # We need to find the movie in the Collaborative DB (MovieLens)
    # This requires fuzzy matching the title (removing year)
    collab_idx = -1
    clean_input_title = clean_title(movie_title)
    
    for idx, t in enumerate(titles_collab):
        if clean_title(t) == clean_input_title:
            collab_idx = idx
            break
            
    # 5. Combine Logic
    if collab_idx != -1:
        # Case A: Movie exists in BOTH databases (Hybrid Mode)
        print(f"✅ Found '{movie_title}' in both databases. Using Hybrid Mode.")
        
        collab_scores = list(enumerate(similarity_collab[collab_idx]))
        
        collab_data = []
        for i, score in collab_scores:
            title = titles_collab[i]
            # Clean title to match with Content DB
            clean_t = clean_title(title)
            collab_data.append({'clean_title': clean_t, 'collab_score': score})
            
        df_collab = pd.DataFrame(collab_data)
        
        # Merge the two dataframes on the cleaned title
        # We first add a clean_title column to df_content
        df_content['clean_title'] = df_content['title'].apply(clean_title)
        
        # Merge (Inner join: we only recommend movies that exist in BOTH for now)
        # You could use Outer join to include content-only matches with 0 collab score
        df_hybrid = pd.merge(df_content, df_collab, on='clean_title', how='left')
        
        # Fill NaN collab scores with 0 (for movies not in collab DB)
        df_hybrid['collab_score'] = df_hybrid['collab_score'].fillna(0)
        
        # Calculate Hybrid Score
        # Weight: 60% Content (Metadata), 40% Collab (User Ratings)
        # You can tweak this!
        df_hybrid['hybrid_score'] = (df_hybrid['content_score'] * 0.6) + (df_hybrid['collab_score'] * 0.4)
        
        # Sort
        recommendations = df_hybrid.sort_values('hybrid_score', ascending=False)
        
    else:
        # Case B: Movie only in Content DB (New or Obscure movie)
        print(f"⚠️ '{movie_title}' not found in Collaborative DB. Falling back to Content-Only.")
        recommendations = df_content.sort_values('content_score', ascending=False)

    # 6. Return Top N (excluding the input movie itself)
    # We filter out the exact title match to avoid recommending the same movie
    final_recs = recommendations[recommendations['title'].str.lower() != movie_title.lower()]
    
    return final_recs['title'].head(top_n).tolist()

if __name__ == "__main__":
    # Test Hybrid
    movie = "Toy Story"
    print(f"\n🧠 Hybrid Recommendations for '{movie}':")
    print(get_hybrid_recommendations(movie))
    
    # Test Fallback (A movie likely not in the small MovieLens dataset or named differently)
    movie2 = "Avatar" 
    print(f"\n🧠 Recommendations for '{movie2}':")
    print(get_hybrid_recommendations(movie2))