import { useEffect, useState } from 'react';
import { getMovieDetails } from '../api';
import { Star, Calendar } from 'lucide-react';

const MovieCard = ({ movie, reason }) => {
    const [details, setDetails] = useState(null);

    useEffect(() => {
        const fetchDetails = async () => {
            if (movie.id) {
                const data = await getMovieDetails(movie.id);
                setDetails(data);
            }
        };
        fetchDetails();
    }, [movie.id]);

    const imageUrl = details?.poster_path
        ? `https://image.tmdb.org/t/p/w500${details.poster_path}`
        : "https://via.placeholder.com/500x750?text=No+Image";

    return (
        <div className="group relative bg-[#121212] rounded-xl overflow-hidden shadow-xl hover:shadow-2xl hover:shadow-red-900/20 transition-all duration-300 transform hover:-translate-y-2 animate-fade-in">
            {/* Image Container with Glow Effect */}
            <div className="aspect-[2/3] overflow-hidden relative">
                <img
                    src={imageUrl}
                    alt={movie.title}
                    className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500"
                />
                {/* Dark Gradient Overlay for text readability */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent opacity-60 group-hover:opacity-80 transition-opacity" />
            </div>

            {/* Content Area */}
            <div className="absolute bottom-0 left-0 right-0 p-4 transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300">
                <h3 className="text-lg font-bold text-white mb-1 leading-tight drop-shadow-md">
                    {movie.title}
                </h3>

                <div className="flex items-center gap-3 text-xs text-gray-300 mb-3">
                    <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-red-500" />
                        {details?.release_date?.split('-')[0] || 'N/A'}
                    </span>
                    <span className="flex items-center gap-1">
                        <Star className="w-3 h-3 text-yellow-500" />
                        {details?.vote_average?.toFixed(1) || 'N/A'}
                    </span>
                </div>

                {/* The "Why" Badge - Premium Glass Look */}
                <div className="bg-white/10 backdrop-blur-md border border-white/10 p-2 rounded-lg text-xs text-gray-200">
                    <span className="text-red-400 font-semibold uppercase tracking-wider text-[10px]">Because you liked it:</span>
                    <p className="mt-1 line-clamp-2 leading-relaxed opacity-90">{reason}</p>
                </div>
            </div>
        </div>
    );
};

export default MovieCard;