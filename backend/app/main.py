from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import os
import requests

# Initialize App
app = FastAPI(title="Cinephile Recommender API")

# CORS (Cross-Origin Resource Sharing)
# This allows our React frontend (running on port 3000) to talk to this backend (on port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Variables to hold our models ---
models = {}
movies_df = None

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models")

# --- Startup Event ---
@app.on_event("startup")
def load_models():
    """
    Load models into memory when server starts.
    This prevents reloading 500MB files on every request.
    """
    global models, movies_df
    try:
        print("⏳ Loading models...")
        models['content_list'] = pickle.load(open(os.path.join(MODEL_PATH, 'movie_list.pkl'), 'rb'))
        models['content_sim'] = pickle.load(open(os.path.join(MODEL_PATH, 'similarity.pkl'), 'rb'))
        
        # Collaborative models
        models['collab_sim'] = pickle.load(open(os.path.join(MODEL_PATH, 'collab_similarity.pkl'), 'rb'))
        models['collab_titles'] = pickle.load(open(os.path.join(MODEL_PATH, 'collab_titles.pkl'), 'rb'))
        
        # Load the raw dataframe to get Poster IDs
        # We need the original TMDB CSV for 'id' and 'overview'
        # Optimizing: Let's reuse the pickled content_list since it has titles
        # But we need 'movie_id' for posters. 
        # In Phase 2, we saved 'movie_id' in movie_list.pkl. Perfect.
        movies_df = models['content_list']
        
        print("✅ Models Loaded Successfully!")
    except Exception as e:
        print(f"❌ Error loading models: {e}")

# --- Helper Functions ---

def fetch_poster(movie_id):
    """
    Constructs the TMDB image URL.
    Note: Ideally, you'd use the TMDB API to get the *latest* path, 
    but for this portfolio project, we can try to fetch it or use a placeholder.
    
    Since our CSV doesn't have the full path, we will use a trick:
    We'll return the ID and let the Frontend fetch the image from TMDB API 
    (which is cleaner for the backend).
    """
    return f"https://image.tmdb.org/t/p/w500/" 
    # Actually, we need the specific 'poster_path' (e.g., /uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg).
    # Since we don't have that in our processed pickle, we will return the ID 
    # and handle the specific image fetching in the frontend or 
    # we can do a quick lookup if we load the raw CSV.
    
    # FOR SIMPLICITY: We will rely on the Frontend to hit the TMDB API using the movie_id.
    return movie_id

def get_recommendations_logic(movie_title):
    # This mirrors the logic in hybrid_engine.py
    # For simplicity in this tutorial, we will implement a direct Content-Based call here 
    # to ensure it works 100% without complex merging errors, then upgrade.
    
    # 1. Find Movie Index
    try:
        idx = movies_df[movies_df['title'].str.lower() == movie_title.lower()].index[0]
    except IndexError:
        return []

    # 2. Get Similarity
    distances = models['content_sim'][idx]
    
    # 3. Sort
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]
    
    results = []
    for i in movie_list:
        movie_idx = i[0]
        row = movies_df.iloc[movie_idx]
        
        results.append({
            "id": int(row['movie_id']),
            "title": row['title'],
            "match_score": f"{round(i[1]*100)}%",
            "reason": "Based on plot, cast, and director similarity."
        })
    
    return results

# --- API Endpoints ---

class RecommendationRequest(BaseModel):
    title: str

@app.get("/")
def home():
    return {"message": "Cinephile API is Running 🚀"}

@app.post("/recommend")
def recommend(request: RecommendationRequest):
    print(f"🔍 Recommendation request for: {request.title}")
    
    recommendations = get_recommendations_logic(request.title)
    
    if not recommendations:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    return {
        "movie": request.title,
        "recommendations": recommendations
    }

# To run: uvicorn app.main:app --reload