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

    def explore_my_playlist(self, playlist_id='2pg3LPneBfKIpyAUH0jdjp'):
        playlist = self.sp.playlist(playlist_id)
        print(f"\n=== Exploring Playlist: {playlist['name']} ===")
        
        print("\nTop Tracks in Your Playlist:")
        for i, item in enumerate(playlist['tracks']['items'][:10], 1):
            track = item['track']
            print(f"{i}. {track['name']} by {track['artists'][0]['name']}")

    def enhanced_recommendations(self):
        print("\n=== Enhanced Music Recommendation Engine ===")
        print("Choose your recommendation source:")
        print("1. Search by Song")
        print("2. Use Your Playlist")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == '1':
            print("Available moods: happy, sad, energetic, chill, party")
            song_name = input("\nEnter a song you like: ")
            mood = input("Enter your desired mood: ").lower()
            
            results = self.sp.search(q=song_name, type='track', limit=1)
            if not results['tracks']['items']:
                print("Song not found!")
                return
            
            track = results['tracks']['items'][0]
            artist_id = track['artists'][0]['id']
            
            top_tracks = self.sp.artist_top_tracks(artist_id)
            
            print(f"\nRecommended tracks based on {track['name']}:")
            for i, rec in enumerate(top_tracks['tracks'][:5], 1):
                print(f"{i}. {rec['name']} by {rec['artists'][0]['name']}")
                
        elif choice == '2':
            playlist = self.sp.playlist('596GIcpIGocwj41T0zcn7d')
            seed_track = playlist['tracks']['items'][0]['track']
            artist_id = seed_track['artists'][0]['id']
            
            print(f"\nRecommendations based on your playlist:")
            recommendations = self.sp.artist_top_tracks(artist_id)
            
            for i, track in enumerate(recommendations['tracks'][:5], 1):
                print(f"{i}. {track['name']} by {track['artists'][0]['name']}")

def main():
    spotify_client = SpotifyClient()
    spotify_client.get_top_artists(limit=5)
    spotify_client.get_playlist(limit=5)
    spotify_client.get_top_tracks(limit=10)
    spotify_client.get_recent_tracks(limit=50)
    spotify_client.explore_my_playlist()
    spotify_client.enhanced_recommendations()

if __name__ == "__main__":
    main()

