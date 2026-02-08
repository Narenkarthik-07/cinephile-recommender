import { useState } from 'react';
import { Search, Film, Sparkles, Menu } from 'lucide-react';
import { getRecommendations } from './api';
import MovieCard from './components/MovieCard';

function App() {
  const [query, setQuery] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError("");
    setRecommendations([]);
    setHasSearched(true);

    const data = await getRecommendations(query);

    if (data && data.recommendations) {
      setRecommendations(data.recommendations);
    } else {
      setError("SorryMovie not found, We have a limited database. Please try another title.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen text-white font-sans selection:bg-red-500 selection:text-white">

      {/* Navbar - Glassmorphism */}
      <nav className="fixed top-0 w-full z-50 px-6 py-4 flex justify-between items-center bg-black/50 backdrop-blur-lg border-b border-white/5">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-red-600 to-red-900 rounded-lg flex items-center justify-center shadow-lg shadow-red-500/20">
            <Film className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight">Cinephile<span className="text-red-500">.AI</span></span>
        </div>
        <button className="p-2 hover:bg-white/10 rounded-full transition-colors">
          <Menu className="w-6 h-6 text-gray-300" />
        </button>
      </nav>

      {/* Main Content Area */}
      <div className={`relative transition-all duration-700 ease-in-out flex flex-col items-center ${hasSearched ? 'pt-32' : 'justify-center min-h-[80vh]'}`}>

        {/* Hero Section */}
        <div className="text-center px-4 w-full max-w-4xl mx-auto z-10">
          {!hasSearched && (
            <div className="mb-8 animate-fade-in">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm text-gray-400 mb-6 backdrop-blur-sm">
                <Sparkles className="w-4 h-4 text-yellow-400" />
                <span>Powered by Hybrid AI Filtering</span>
              </div>
              <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-white to-gray-400">
                What to watch next?
              </h1>
              <p className="text-lg text-gray-400 max-w-2xl mx-auto leading-relaxed">
                Stop scrolling for hours. Let our AI analyze plot, cast, and user ratings to find your perfect match.
              </p>
            </div>
          )}

          {/* Premium Search Bar */}
          <form onSubmit={handleSearch} className="w-full max-w-2xl mx-auto relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-red-600 to-red-900 rounded-full blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200" />
            <div className="relative flex items-center bg-[#1a1a1a] rounded-full p-2 border border-white/10 shadow-2xl focus-within:border-red-500/50 focus-within:ring-2 focus-within:ring-red-500/20 transition-all">
              <Search className="w-6 h-6 text-gray-500 ml-4" />
              <input
                type="text"
                placeholder="Enter a movie "
                className="w-full bg-transparent border-none text-white text-lg px-4 py-3 focus:ring-0 placeholder-gray-500"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-white text-black px-8 py-3 rounded-full font-bold hover:bg-gray-200 transition-transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <div className="w-5 h-5 border-2 border-black border-t-transparent rounded-full animate-spin" />
                ) : (
                  "Generate"
                )}
              </button>
            </div>
          </form>

          {/* Cold Start Note */}
          {!hasSearched && !loading && (
            <div className="mt-4 text-xs text-gray-500 bg-black/30 px-4 py-2 rounded-full inline-block border border-white/5 backdrop-blur-sm">
              <span className="text-yellow-500 font-bold">⚠️ Note:</span> First search may take 10-20s to wake up the free server.
            </div>
          )}

          {/* Loading State Message */}
          {loading && (
            <div className="mt-4 text-sm text-gray-400 animate-pulse">
              Waking up the AI brain... this might take a moment.
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-4 p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-red-200 max-w-md mx-auto animate-fade-in">
              {error}
            </div>
          )}
        </div>
      </div>

      {/* Results Grid */}
      {recommendations.length > 0 && (
        <div className="container mx-auto px-6 pb-20 mt-12 animate-fade-in">
          <div className="flex items-center gap-4 mb-8">
            <div className="h-8 w-1 bg-red-500 rounded-full" />
            <h2 className="text-2xl font-bold tracking-wide">Curated For You</h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {recommendations.map((rec) => (
              <MovieCard key={rec.id} movie={rec} reason={rec.reason} />
            ))}
          </div>
        </div>
      )}

      {/* Footer Decoration */}
      <div className="fixed bottom-0 left-0 w-full h-32 bg-gradient-to-t from-black to-transparent pointer-events-none z-0" />
    </div>
  );
}

export default App;