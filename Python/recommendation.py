import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="f3118b77a7154acb899ec1d17391c04c",
            client_secret="7797aa9c0c284fab822a42b3869449bf",
            redirect_uri="http://localhost:3000/callback",
            scope="user-top-read user-read-recently-played playlist-read-private user-library-read playlist-modify-public"
        ))

    def get_top_artists(self, limit=5, time_range='long_term'):
        top_artists = self.sp.current_user_top_artists(limit=limit, time_range=time_range)
        print(f"\nReal-Time Top {limit} Artists/Groups:\n")
        for idx, artist in enumerate(top_artists['items'], 1):
            artist_name = artist['name']
            genres = ', '.join(artist['genres'])
            print(f"{idx}. {artist_name} (Genres: {genres})")

    def get_recent_tracks(self, limit=50, time_range="medium_term"):
        recent_tracks = self.sp.current_user_recently_played(limit=limit)
        print(f"\nMost Recent {limit} Tracks Played:\n")
        for idx, item in enumerate(recent_tracks['items'], 1):
            track = item['track']
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            played_at = item['played_at']
            print(f"{idx}. {track_name} by {artist_name} (Played at: {played_at})")

    def get_top_tracks(self, limit=10, time_range="short_term"):
        top_tracks = self.sp.current_user_top_tracks(limit=limit, time_range=time_range)
        print(f"\nTop {limit} Tracks:\n")
        for idx, track in enumerate(top_tracks['items'], 1):
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            print(f"{idx}. {track_name} by {artist_name}")

    def get_playlist(self, limit=5):
        playlists = self.sp.current_user_playlists(limit=limit)
        print(f"\nUser's Playlists (Showing {limit}):\n")
        if not playlists['items']:
            print("No playlists found.")
            return
        
        for idx, playlist in enumerate(playlists['items'], 1):
            playlist_name = playlist['name']
            playlist_id = playlist['id']
            num_tracks = playlist['tracks']['total']
            print(f"{idx}. {playlist_name} (ID: {playlist_id}, Total Tracks: {num_tracks})")

    def interactive_recommendations(self):
        print("\n=== Music Recommendation Engine ===")
        print("Available moods: happy, sad, energetic, chill, party")
        
        song_name = input("\nEnter a song you like: ")
        mood = input("Enter your desired mood: ").lower()
        
        results = self.sp.search(q=song_name, type='track', limit=1)
        if not results['tracks']['items']:
            print("Song not found!")
            return
        
        track = results['tracks']['items'][0]
        print(f"\nGetting recommendations based on {track['name']} by {track['artists'][0]['name']}")
        print(f"Mood: {mood}")
        
        mood_presets = {
            'happy': {'valence': 0.7, 'energy': 0.7, 'danceability': 0.7}, 
            'sad': {'valence': 0.3, 'energy': 0.3, 'danceability': 0.4},
            'energetic': {'energy': 0.8, 'tempo': 120, 'danceability': 0.8},
            'chill': {'energy': 0.3, 'tempo': 90, 'acousticness': 0.7},
            'party': {'danceability': 0.8, 'energy': 0.8, 'valence': 0.7}
        }

        recommendations = self.sp.recommendations(
            seed_tracks=[track['id']],
            target_valence=mood_presets.get(mood, {}).get('valence'),
            target_energy=mood_presets.get(mood, {}).get('energy'),
            target_danceability=mood_presets.get(mood, {}).get('danceability'),
            limit=5
        )

        print("\nRecommended tracks:")
        for idx, rec in enumerate(recommendations['tracks'], 1):
            print(f"{idx}. {rec['name']} by {rec['artists'][0]['name']}")

# Create instance and run all features
spotify_client = SpotifyClient()
spotify_client.get_top_artists(limit=5)
spotify_client.get_playlist(limit=5)
spotify_client.get_top_tracks(limit=10)
spotify_client.get_recent_tracks(limit=50)
spotify_client.interactive_recommendations()
