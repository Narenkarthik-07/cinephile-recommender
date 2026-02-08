import { useState } from 'react';
import { Search, Film } from 'lucide-react';
import { getRecommendations } from './api';
import MovieCard from './components/MovieCard';

function App() {
  const [query, setQuery] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query) return;

    setLoading(true);
    setError("");
    setRecommendations([]);

    const data = await getRecommendations(query);

    if (data && data.recommendations) {
      setRecommendations(data.recommendations);
    } else {
      setError("Sorry Movie not found, We have . Try another title!");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-cinema-900 text-white pb-20">
      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center py-20 px-4 text-center bg-gradient-to-b from-black to-cinema-900">
        <Film className="w-16 h-16 text-cinema-500 mb-4" />
        <h1 className="text-5xl font-extrabold mb-4 tracking-tight">
          Cinephile <span className="text-cinema-500">AI</span>
        </h1>
        <p className="text-gray-400 text-lg max-w-xl mb-8">
          Discover your next favorite film. Powered by Hybrid AI (Content + Collaborative Filtering).
        </p>

        {/* Search Bar */}
        <form onSubmit={handleSearch} className="w-full max-w-lg relative">
          <input
            type="text"
            placeholder="Enter a movie you Enjoyed"
            className="w-full py-4 px-6 pl-12 rounded-full bg-cinema-800 text-white border border-gray-700 focus:border-cinema-500 focus:outline-none focus:ring-2 focus:ring-cinema-500/50 transition-all text-lg shadow-xl"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />

          <button
            type="submit"
            disabled={loading}
            className="absolute right-2 top-2 bottom-2 px-6 bg-cinema-500 hover:bg-red-700 rounded-full font-bold transition-colors disabled:opacity-50"
          >
            {loading ? "..." : "Recommend"}
          </button>
        </form>

        {error && <p className="mt-4 text-red-400">{error}</p>}
      </div>

      {/* Results Section */}
      {recommendations.length > 0 && (
        <div className="container mx-auto px-6">
          <h2 className="text-2xl font-bold mb-6 border-l-4 border-cinema-500 pl-4">
            Recommended for you
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
            {recommendations.map((rec) => (
              <MovieCard key={rec.id} movie={rec} reason={rec.reason} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;