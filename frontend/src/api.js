import axios from 'axios';

const API_KEY = "cc0eb85c785d3c9137af68a8c4c9c538"; // Free Tier Key Exposed for Demo Purposes
const BASE_URL = "https://api.themoviedb.org/3";
const BACKEND_URL = "https://cinephile-ai.onrender.com";

// 1. Get Recommendations from OUR Backend
export const getRecommendations = async (title) => {
    try {
        const response = await axios.post(`${BACKEND_URL}/recommend`, { title });
        return response.data;
    } catch (error) {
        console.error("Backend Error:", error);
        return null;
    }
};

// 2. Get Movie Details (Poster) from TMDB
export const getMovieDetails = async (movieId) => {
    try {
        const response = await axios.get(`${BASE_URL}/movie/${movieId}?api_key=${API_KEY}`);
        return response.data;
    } catch (error) {
        console.error("TMDB Error:", error);
        return null; // Return null if image not found
    }
};