import React, { useState } from "react";
import RecommendationSearchComponent from "../Components/backend/RecommendationSearchComponent";
import "./RecommendationSearchPage.css";

const RecommendationSearchPage = () => {
    const backendUrl = "http://localhost:8000"; // Backend URL
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
            <RecommendationSearchComponent
                backendUrl={backendUrl}
                mode={modeDetails[mode].mode}
                placeholder={modeDetails[mode].placeholder}
            />
        </div>
    );
};

export default RecommendationSearchPage;
