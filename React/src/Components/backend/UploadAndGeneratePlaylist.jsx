import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import TracksList from "../spotify-data/track-display/tracks-list.jsx";
import TrackHTML from "../spotify-data/track-display/track-container.jsx";

const UploadAndGeneratePlaylist = ({ authToken }) => {
    const recentlyPlayedLink = "https://api.spotify.com/v1/me/player/recently-played";
    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

    const [isLoadingHistory, setLoadingHistory] = useState(true);
    const [historyData, setHistoryData] = useState([]);
    const [playlistName, setPlaylistName] = useState("Peepify Playlist");
    const [songLimit, setSongLimit] = useState(30);
    const [statusMessage, setStatusMessage] = useState("");

    useEffect(() => {
        fetchRecentlyPlayed();
    }, []);

    const fetchRecentlyPlayed = async () => {
        try {
            const response = await fetch(recentlyPlayedLink, {
                method: "GET",
                headers: authHeader,
            });

            setLoadingHistory(false);

            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const json = await response.json();
            setHistoryData(json.items); // Extract the "items" array containing track details
        } catch (error) {
            console.log("API error: ", error);
        }
    };

    const handleGeneratePlaylist = async () => {
        try {
            const response = await fetch("http://localhost:8000/dynamic_playlist/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    playlist_name: playlistName, // Name of the playlist
                    song_limit: songLimit, // Limit for the number of songs
                }),
            });

            if (!response.ok) {
                throw new Error(`Failed with status: ${response.status}`);
            }

            const result = await response.json();
            if (result.status === "success") {
                console.log("Playlist created successfully:", result.message);
            } else {
                console.error("Failed to create playlist:", result.message);
            }
        } catch (error) {
            console.error("Error generating playlist:", error);
        }
    };


    return (
        <div className="playlist-generator">
            <h2>Generate Dynamic Playlist from Recently Played</h2>
            {isLoadingHistory ? (
                <p>Loading recently played tracks...</p>
            ) : (
                <>
                    <div>
                        <label>
                            <strong>Playlist Name:</strong>
                            <input
                                type="text"
                                value={playlistName}
                                onChange={(e) => setPlaylistName(e.target.value)}
                            />
                        </label>
                    </div>
                    <div>
                        <label>
                            <strong>Song Limit:</strong>
                            <input
                                type="number"
                                value={songLimit}
                                onChange={(e) => setSongLimit(Number(e.target.value))}
                                min="1"
                            />
                        </label>
                    </div>
                    <button onClick={handleGeneratePlaylist}>Generate Playlist</button>
                    {statusMessage && <p>{statusMessage}</p>}
                    <h3>Recently Played Tracks:</h3>
                    <TracksList>
                        {historyData.map((item) => (
                            <TrackHTML
                                key={`${item.track.id}${item.played_at}`}
                                imageLink={item.track.album.images[0].url}
                                artists={item.track.artists}
                                name={item.track.name}
                                when={item.played_at}
                                length={item.track.duration_ms}
                            />
                        ))}
                    </TracksList>
                </>
            )}
        </div>
    );
};

UploadAndGeneratePlaylist.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default UploadAndGeneratePlaylist;
