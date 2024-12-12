import React, { useState } from "react";
import RecommendationSearchComponent from "../Components/backend/RecommendationSearchComponent"; // Adjust path
import "./RecommendationSearchPage.css"; // Ensure styles are properly scoped

const RecommendationSearchPage = () => {
    const backendUrl = "http://localhost:8000"; // Replace with your backend URL
    const [mode, setMode] = useState("song");

    const handleModeChange = (newMode) => {
        setMode(newMode);
    };

    const modeDetails = {
        song: { placeholder: "Enter a song name...", mode: "song" },
        artist: { placeholder: "Enter an artist name...", mode: "artist" },
        genre: { placeholder: "Enter a genre...", mode: "genre" },
    };

    return (
        <div className="recommendation-search-page">
            <div className="mode-buttons">
                <button
                    className={mode === "song" ? "active" : ""}
                    onClick={() => handleModeChange("song")}
                >
                    Song
                </button>
                <button
                    className={mode === "artist" ? "active" : ""}
                    onClick={() => handleModeChange("artist")}
                >
                    Artist
                </button>
                <button
                    className={mode === "genre" ? "active" : ""}
                    onClick={() => handleModeChange("genre")}
                >
                    Genre
                </button>
            </div>
            <div className="recommendation-content">
                <RecommendationSearchComponent
                    backendUrl={backendUrl}
                    mode={modeDetails[mode].mode}
                    placeholder={modeDetails[mode].placeholder}
                />
            </div>
        </div>
    );
};

export default RecommendationSearchPage;
