from fastapi import FastAPI
from spotify_client import SpotifyClient
from data_analysis import DataAnalysis

# Initialize the app and classes
app = FastAPI()
spotify_client = SpotifyClient()
data_analysis = DataAnalysis(spotify_client)

# API Endpoints
@app.get("/api/recent-tracks")
def get_recent_tracks(limit: int = 50):
    spotify_client.fetch_recent_tracks(limit=limit)
    return {"recentTracks": [
        {
            "trackName": track["track"]["name"],
            "artistName": track["track"]["artists"][0]["name"],
            "playedAt": track["played_at"],
        }
        for track in spotify_client.recent_tracks_data["items"]
    ]}

@app.get("/api/top-artists")
def get_top_artists(limit: int = 10):
    spotify_client.fetch_top_artists(limit=limit)
    return {"topArtists": [
        {
            "artistName": artist["name"],
            "genres": artist.get("genres", []),
            "popularity": artist.get("popularity", 0),
        }
        for artist in spotify_client.top_artists_data["items"]
    ]}

@app.get("/api/dynamic-playlist")
def create_dynamic_playlist():
    data_analysis.dynamic_playlist(playlist_name="Peepify Playlist", song_limit=50)
    return {"message": "Dynamic playlist created or updated successfully."}

@app.get("/api/streaming-history")
def get_streaming_history():
    spotify_client.extract_and_load_json()
    return {"streamingHistory": [
        {
            "trackName": track.get("trackName"),
            "artistName": track.get("artistName"),
            "playedAt": track.get("endTime"),
        }
        for track in spotify_client.streaming_history_data
    ]}
