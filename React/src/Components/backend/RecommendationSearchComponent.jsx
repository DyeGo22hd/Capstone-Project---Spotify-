import React, { useState } from "react";
import PropTypes from "prop-types";
import './RecommendationSearchComponent.css';

const RecommendationSearchComponent = ({ backendUrl, mode, placeholder }) => {
    const [searchQuery, setSearchQuery] = useState("");
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState("");

    const handleSearch = async () => {
        if (!searchQuery.trim()) {
            setError(`Please enter a ${mode} name.`);
            return;
        }

        setError(""); // Clear any previous error

        try {
            const response = await fetch(`${backendUrl}/api/recommendations/by-${mode}?${mode}_name=${encodeURIComponent(searchQuery)}`);

            if (!response.ok) {
                throw new Error(`Failed to fetch recommendations: ${response.statusText}`);
            }

            const data = await response.json();
            setRecommendations(data.recommendations || []);
        } catch (err) {
            console.error(err);
            setError("An error occurred while fetching recommendations.");
        }
    };

    return (
        <div className="recommendation-search-component">
            <div className="search-box">
                <input
                    type="text"
                    placeholder={placeholder}
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
                <button onClick={handleSearch}>Search</button>
            </div>
            {error && <p className="error-message">{error}</p>}
            {recommendations.length > 0 && (
                <div className="recommendations">
                    <h3>Recommendations:</h3>
                    <ul>
                        {recommendations.map((rec, index) => (
                            <li key={index}>
                                <strong>{rec.trackName}</strong> by {rec.artistName}
                                <br />
                                <em>{rec.albumName}</em>
                                <br />
                                <a href={rec.spotifyUrl} target="_blank" rel="noopener noreferrer">
                                    Listen on Spotify
                                </a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

RecommendationSearchComponent.propTypes = {
    backendUrl: PropTypes.string.isRequired,
    mode: PropTypes.string.isRequired, // E.g., 'song', 'artist', or 'genre'
    placeholder: PropTypes.string, // Placeholder for the search input
};

RecommendationSearchComponent.defaultProps = {
    placeholder: "Search...",
};

export default RecommendationSearchComponent;
