import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

class SpotifyClient:
    def __init__(self):
        # Set up Spotify OAuth with your credentials and redirect URI
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="a1b69bc66206450b90556539dce74413",
            client_secret="fb50ad80e74840968e1e3047174a3ae2",
            redirect_uri="http://localhost:3000/callback",
            scope="user-top-read user-read-recently-played playlist-read-private"
        ))

    def get_top_artists(self, limit=5, time_range='long_term'):
    
        # Fetch top artists data from Spotify API
        top_artists = self.sp.current_user_top_artists(limit=limit, time_range=time_range)
        
        # Display top artists
        print(f"\nReal-Time Top {limit} Artists/Groups:\n")
        for idx, artist in enumerate(top_artists['items'], 1):
            artist_name = artist['name']
            genres = ', '.join(artist['genres'])
            print(f"{idx}. {artist_name} (Genres: {genres})")

    
    def get_recent_tracks(self, limit=50, time_range="medium_term"):
        # Fetch the user's recently played tracks
        recent_tracks = self.sp.current_user_recently_played(limit=limit)
        
        # Display recent tracks
        print(f"\nMost Recent {limit} Tracks Played:\n")
        for idx, item in enumerate(recent_tracks['items'], 1):
            track = item['track']
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            played_at = item['played_at']
            print(f"{idx}. {track_name} by {artist_name} (Played at: {played_at})")


    def get_top_tracks(self, limit=10, time_range="short_term"):
        # Fetch the user's top tracks
        top_tracks = self.sp.current_user_top_tracks(limit=limit, time_range=time_range)

        # Print top tracks
        print(f"\nTop {limit} Tracks:\n")
        for idx, track in enumerate(top_tracks['items'], 1):
            artist_name = track['artists'][0]['name']  # Artist's name
            track_name = track['name']                 # Track's name
            print(f"{idx}. {track_name} by {artist_name}")
            

    
    def get_playlist(self, limit=5):
         # Fetch the user's playlists
       
        playlists = self.sp.current_user_playlists(limit=limit)
        
        
        # Display playlists
        print(f"\nUser's Playlists (Showing {limit}):\n")
        if not playlists['items']:
            print("No playlists found.")
            return
    
            
        for idx, playlist in enumerate(playlists['items'], 1):
            playlist_name = playlist['name']
            playlist_id = playlist['id']
            num_tracks = playlist['tracks']['total']
            print(f"{idx}. {playlist_name} (ID: {playlist_id}, Total Tracks: {num_tracks})")

    

    


# Instantiate SpotifyClient and fetch real-time top artists
spotify_client = SpotifyClient()
spotify_client.get_top_artists(limit=5)
spotify_client.get_playlist(limit=5)
spotify_client.get_top_tracks(limit=10)
spotify_client.get_recent_tracks(limit=50)