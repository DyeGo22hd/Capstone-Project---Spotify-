from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from spotify_client import SpotifyClient
from data_analysis import DataAnalysis
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust for your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate Spotify client and data analysis objects
spotify_client = SpotifyClient()
data_analysis = DataAnalysis(spotify_client)

@app.get("/")
def root():
    return {"message": "API is working"}


@app.post("/upload/")
async def upload_json(file: UploadFile, file_type: str = Form(...)):
    """
    Endpoint to upload JSON files for streaming or extended history.
    Saves the JSON data into the database for the current user.
    
    Args:
        file: The uploaded JSON file.
        file_type: The type of the file (e.g., 'streamingHistory', 'extendedHistory').
    """
    try:
        # Read the uploaded file content
        file_content = await file.read()
        file_path = f"/tmp/{file.filename}"

        # Save the content temporarily for processing
        with open(file_path, "wb") as temp_file:
            temp_file.write(file_content)

        # Process the JSON file with the Spotify client
        spotify_client.extract_and_load_json(file_path)

        # Remove the temporary file
        os.remove(file_path)

        return {"status": "success", "message": f"Uploaded {file_type} data successfully."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/filter_tracks/")
def filter_tracks(file_type: str, year: int, month: int):
    """
    Endpoint to filter tracks from JSON data by a specified year and month.
    
    Args:
        file_type: The type of data to filter ('streamingHistory' or 'extendedHistory').
        year: The year to filter from.
        month: The month to filter from.
    """
    try:
        tracks = spotify_client.filter_tracks_by_date(file_type, year, month)
        return {"filtered_tracks": tracks}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/top_artists/")
def get_top_artists(limit: int = 5, time_range: str = "short_term"):
    """
    Endpoint to fetch the user's top artists from Spotify.
    
    Args:
        limit: The number of top artists to fetch.
        time_range: The time range for fetching top artists (e.g., 'short_term', 'long_term').
    """
    try:
        top_artists = spotify_client.fetch_top_artists(limit=limit, time_range=time_range)
        return {"top_artists": top_artists}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/recent_tracks/")
def get_recent_tracks(limit: int = 50):
    """
    Endpoint to fetch the user's recent tracks from Spotify.
    
    Args:
        limit: The number of recent tracks to fetch.
    """
    try:
        recent_tracks = spotify_client.fetch_recent_tracks(limit=limit)
        return {"recent_tracks": recent_tracks}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/dynamic_playlist/")
def create_playlist(playlist_name: str = "Peepify Playlist", song_limit: int = 30):
    """
    Endpoint to generate a dynamic playlist based on the user's listening history.
    
    Args:
        playlist_name: The name of the playlist to create.
        song_limit: The maximum number of songs in the playlist.
    """
    try:
        data_analysis.dynamic_playlist(playlist_name, song_limit)
        return {"status": "success", "message": f"Playlist '{playlist_name}' created."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@app.get("/api/recommendations/all-genres")
def get_available_genres():
    popular_genres = ['pop', 'rock', 'hip-hop', 'dance', 'indie', 'electronic', 'r&b', 'jazz', 'classical', 'metal']
    return {"genres": popular_genres}

@app.get("/api/recommendations/by-song")
def get_recommendations_by_song(song_name: str):
    results = spotify_client.sp.search(q=song_name, type='track', limit=5)
    return {
        "recommendations": [
            {
                "trackName": track['name'],
                "artistName": track['artists'][0]['name'],
                "albumName": track['album']['name'],
                "spotifyUrl": track['external_urls']['spotify']
            }
            for track in results['tracks']['items']
        ]
    }

@app.get("/api/recommendations/by-artist")
def get_recommendations_by_artist(artist_name: str):
    results = spotify_client.sp.search(q=artist_name, type='track', limit=5)
    return {
        "recommendations": [
            {
                "trackName": track['name'],
                "artistName": track['artists'][0]['name'],
                "albumName": track['album']['name'],
                "spotifyUrl": track['external_urls']['spotify']
            }
            for track in results['tracks']['items']
        ]
    }

@app.get("/api/recommendations/by-genre")
def get_recommendations_by_genre(genre: str):
    results = spotify_client.sp.search(q=f"genre:{genre}", type='track', limit=5)
    return {
        "recommendations": [
            {
                "trackName": track['name'],
                "artistName": track['artists'][0]['name'],
                "albumName": track['album']['name'],
                "spotifyUrl": track['external_urls']['spotify']
            }
            for track in results['tracks']['items']
        ]
    }

@app.get("/api/recommendations/by-mood")
def get_recommendations_by_mood(mood: str):
    mood_queries = {
        'happy': 'genre:pop year:2023',
        'sad': 'genre:indie year:2023',
        'energetic': 'genre:dance year:2023',
        'chill': 'genre:chill year:2023'
    }
    
    query = mood_queries.get(mood.lower(), 'genre:pop year:2023')
    results = spotify_client.sp.search(q=query, type='track', limit=5)
    
    return {
        "recommendations": [
            {
                "trackName": track['name'],
                "artistName": track['artists'][0]['name'],
                "albumName": track['album']['name'],
                "spotifyUrl": track['external_urls']['spotify']
            }
            for track in results['tracks']['items']
        ]
    }

@app.get("/api/recommendations/top-tracks")
def get_recommendations_from_top_tracks(limit: int = 5):
    results = spotify_client.sp.search(q="year:2023", type='track', limit=limit)
    return {
        "recommendations": [
            {
                "trackName": track['name'],
                "artistName": track['artists'][0]['name'],
                "albumName": track['album']['name'],
                "spotifyUrl": track['external_urls']['spotify']
            }
            for track in results['tracks']['items']
        ]
    }

@app.get("/api/recommendations/explore-playlist")
def explore_playlist(playlist_id: str = "6leMB93QeEgApPxzQqF81o"):
    playlist = spotify_client.sp.playlist(playlist_id)
    return {
        "playlistName": playlist['name'],
        "tracks": [
            {
                "trackName": item['track']['name'],
                "artistName": item['track']['artists'][0]['name'],
                "albumName": item['track']['album']['name'],
                "spotifyUrl": item['track']['external_urls']['spotify']
            }
            for item in playlist['tracks']['items'][:10]
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
