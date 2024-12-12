import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import TracksList from "../spotify-data/track-display/tracks-list.jsx";
import TrackHTML from "../spotify-data/track-display/track-container.jsx";
import './UploadAndGeneratePlaylist.css';

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
            setHistoryData(json.items);
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
                    Authorization: `Bearer ${authToken}`, // Send the Spotify token
                },
                body: JSON.stringify({
                    playlist_name: playlistName,
                    song_limit: songLimit,
                }),
            });

            if (!response.ok) {
                throw new Error(`Failed with status: ${response.status}`);
            }

            const result = await response.json();
            if (result.status === "success") {
                console.log("Playlist created successfully:", result.message);
                setStatusMessage("Playlist created successfully!");
            } else {
                console.error("Failed to create playlist:", result.message);
                setStatusMessage("Failed to create playlist.");
            }
        } catch (error) {
            console.error("Error generating playlist:", error);
            setStatusMessage("An error occurred while generating the playlist.");
        }
    };



    const handleUploadJSON = async (e) => {
        const file = e.target.files[0];
        if (!file) {
            setStatusMessage("No file selected.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("file_type", "extendedHistory");

        try {
            const response = await fetch("http://localhost:8000/upload/", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Failed with status: ${response.status}`);
            }

            const result = await response.json();
            if (result.status === "success") {
                console.log("File uploaded successfully:", result.message);
                setStatusMessage("File uploaded successfully!");
            } else {
                console.error("Failed to upload file:", result.message);
                setStatusMessage("Failed to upload file.");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            setStatusMessage("An error occurred while uploading the file.");
        }
    };

    return (
        <div className="playlist-generator">
            <h2>Generate Dynamic Playlist from Recently Played</h2>
            {isLoadingHistory ? (
                <p>Loading recently played tracks...</p>
            ) : (
                <>
                    <div className="control-section">
                        {/* Left Side: Inputs and Generate Playlist Button */}
                        <div className="left-section">
                            <label>
                                <strong>Playlist Name:</strong>
                                <input
                                    type="text"
                                    value={playlistName}
                                    onChange={(e) => setPlaylistName(e.target.value)}
                                    style={{ marginLeft: "10px" }}
                                />
                            </label>
                            <label style={{ marginTop: "10px" }}>
                                <strong>Song Limit:</strong>
                                <input
                                    type="number"
                                    value={songLimit}
                                    onChange={(e) => setSongLimit(Number(e.target.value))}
                                    min="1"
                                    style={{ marginLeft: "10px" }}
                                />
                            </label>
                            <button
                                onClick={handleGeneratePlaylist}
                                style={{ marginTop: "20px" }}
                            >
                                Generate Playlist
                            </button>
                        </div>

                        {/* Right Side: Upload Section */}
                        <div className="right-section">
                            <p>Upload extended history JSON here:</p>
                            <input type="file" accept="application/json" onChange={handleUploadJSON} />
                        </div>
                    </div>
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
