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