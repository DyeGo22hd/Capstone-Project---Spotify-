import spotipy
from spotipy.oauth2 import SpotifyOAuth

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

    def get_recent_tracks(self, limit=50):
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

    def explore_my_playlist(self, playlist_id='6leMB93QeEgApPxzQqF81o'):
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
        print("3. Based on Artist")
        print("4. Based on Genre")
        print("5. Based on Your Top Tracks")
        print("6. Based on Audio Features")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            self._recommend_by_song()
        elif choice == '2':
            self._recommend_by_playlist()
        elif choice == '3':
            self._recommend_by_artist()
        elif choice == '4':
            self._recommend_by_genre()
        elif choice == '5':
            self._recommend_by_top_tracks()
        elif choice == '6':
            self._recommend_by_audio_features()
        else:
            print("Great! Let's try a number between 1-6 for the best experience.")

    def _recommend_by_song(self):
        print("\nLet's find similar songs!")
        song_name = input("Enter a song you like: ")
        
        results = self.sp.search(q=song_name, type='track', limit=5)
        print(f"\nHere are similar tracks you might enjoy:")
        for i, track in enumerate(results['tracks']['items'], 1):
            print(f"{i}. {track['name']} by {track['artists'][0]['name']}")

    def _recommend_by_playlist(self):
        playlists = self.sp.current_user_playlists(limit=5)
        print("\nSelect a playlist:")
        for idx, playlist in enumerate(playlists['items'], 1):
            print(f"{idx}. {playlist['name']}")
        
        try:
            playlist_choice = int(input("\nEnter playlist number: ")) - 1
            if 0 <= playlist_choice < len(playlists['items']):
                playlist = self.sp.playlist(playlists['items'][playlist_choice]['id'])
                results = self.sp.search(
                    q=f"genre:{playlist['name']}", 
                    type='track', 
                    limit=5
                )
                print("\nTracks you might like based on this playlist:")
                for i, track in enumerate(results['tracks']['items'], 1):
                    print(f"{i}. {track['name']} by {track['artists'][0]['name']}")
        except:
            self._get_popular_fallback()

    def _recommend_by_artist(self):
        artist_name = input("\nEnter an artist name: ")
        results = self.sp.search(q=artist_name, type='track', limit=5)
        
        print(f"\nTop tracks you might enjoy:")
        for i, track in enumerate(results['tracks']['items'], 1):
            print(f"{i}. {track['name']} by {track['artists'][0]['name']}")

    def _recommend_by_genre(self):
        print("\nPopular genres:")
        popular_genres = ['pop', 'rock', 'hip-hop', 'dance', 'indie', 'electronic', 'r&b', 'jazz', 'classical', 'metal']
        for i, genre in enumerate(popular_genres, 1):
            print(f"{i}. {genre}")
        
        genre_choice = input("\nEnter a genre from the list: ")
        results = self.sp.search(q=f"genre:{genre_choice}", type='track', limit=5)
        
        print(f"\nTop tracks for {genre_choice}:")
        for i, track in enumerate(results['tracks']['items'], 1):
            print(f"{i}. {track['name']} by {track['artists'][0]['name']}")

    def _recommend_by_top_tracks(self):
        results = self.sp.search(q="year:2023", type='track', limit=5)
        print("\nFresh tracks picked for you:")
        for i, track in enumerate(results['tracks']['items'], 1):
            print(f"{i}. {track['name']} by {track['artists'][0]['name']}")

    def _recommend_by_audio_features(self):
        try:
            print("\nLet's find your perfect sound!")
            mood = input("What's your mood today? (happy/sad/energetic/chill): ").lower()
            
            # Map moods to search queries
            mood_queries = {
                'happy': 'genre:pop year:2023',
                'sad': 'genre:indie year:2023',
                'energetic': 'genre:dance year:2023',
                'chill': 'genre:chill year:2023'
            }
            
            query = mood_queries.get(mood, 'genre:pop year:2023')
            results = self.sp.search(q=query, type='track', limit=5)
            
            print(f"\nPerfect tracks for your {mood} mood:")
            for i, track in enumerate(results['tracks']['items'], 1):
                print(f"{i}. {track['name']} by {track['artists'][0]['name']}")
                
        except Exception as e:
            self._get_popular_fallback()

    def _get_popular_fallback(self):
        results = self.sp.search(q="genre:pop year:2023", type='track', limit=5)
        print("\nHot tracks right now:")
        for i, track in enumerate(results['tracks']['items'], 1):
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
