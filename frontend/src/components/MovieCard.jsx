import { useEffect, useState } from 'react';
import { getMovieDetails } from '../api';

const MovieCard = ({ movie, reason }) => {
    const [details, setDetails] = useState(null);

    useEffect(() => {
        // Fetch high-res poster when component mounts
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
        <div className="bg-cinema-800 rounded-lg overflow-hidden shadow-lg hover:scale-105 transition-transform duration-300">
            <img
                src={imageUrl}
                alt={movie.title}
                className="w-full h-80 object-cover"
            />
            <div className="p-4">
                <h3 className="text-lg font-bold text-white mb-1">{movie.title}</h3>
                <p className="text-sm text-gray-400 mb-2">{details?.release_date?.split('-')[0] || 'N/A'}</p>
                <div className="bg-gray-900 p-2 rounded text-xs text-gray-300 border-l-2 border-cinema-500">
                    <span className="font-semibold text-cinema-500">Why?</span> {reason}
                </div>
            </div>
        </div>
    );
};

export default MovieCard;