import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from datetime import datetime

class SpotifyClient:
    def __init__(self):
        # Set up Spotify OAuth with your credentials and redirect URI
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=" b24b1c78e21f447f8c7dce1d2a9d06c5",
            client_secret="c83d6bbfcf884fc488c664d61600f81e",
            redirect_uri="https://cloud.appwrite.io/v1/account/sessions/oauth2/callback/spotify/66f9aeb700248be20f22",
            scope="user-top-read user-read-recently-played playlist-read-private"
        ))

    def get_top_artists(self, limit=5, time_range='long_term'):
        # Fetch top artists data from Spotify API
        return self.sp.current_user_top_artists(limit=limit, time_range=time_range)

    def display_top_artist(self, limit):
        top_artists = self.get_top_artists(limit=limit)

        print(f"\nReal-Time Top {limit} Artists/Groups:\n")
        for idx, artist in enumerate(top_artists['items'], 1):
            artist_name = artist['name']
            genres = ', '.join(artist['genres'])
            print(f"{idx}. {artist_name} (Genres: {genres})")

    def get_top_tracks(self, limit=10, time_range="short_term"):
        # Fetch the user's top tracks
        return self.sp.current_user_top_tracks(limit=limit, time_range=time_range)

    def display_top_tracks(self, limit):
        top_tracks = self.get_top_tracks(limit)  # Corrected call to get_top_tracks

        # Print top tracks
        print(f"\nTop {limit} Tracks:\n")
        for idx, track in enumerate(top_tracks['items'], 1):
            artist_name = track['artists'][0]['name']  # Artist's name
            track_name = track['name']                 # Track's name
            print(f"{idx}. {track_name} by {artist_name}")

    def get_playlist(self, limit):
        # Fetch the user's playlists
        return self.sp.current_user_playlists(limit=limit)

    def display_playlists(self, limit):
        playlists = self.get_playlist(limit)

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

    def get_recent_tracks(self, limit=50):
        return self.sp.current_user_recently_played(limit=limit)

    def display_recent_tracks(self, limit=50):
        recent_tracks = self.get_recent_tracks(limit) 

        print(f"\nMost Recent {limit} Tracks Played:\n")
        for idx, item in enumerate(recent_tracks['items'], 1):
            track = item['track']
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            played_at = item['played_at']
            print(f"{idx}. {track_name} by {artist_name} (Played at: {played_at})")

#testing a while loop
    # def get_recent_tracks(self, limit=50, before=None):
    #     # Retrieve recent tracks with an optional 'before' timestamp
    #     if before:
    #         return self.sp.current_user_recently_played(limit=limit, before=before)
    #     return self.sp.current_user_recently_played(limit=limit)

    # def get_multiple_recent_tracks(self, total_tracks=200, batch_size=50):
    #     all_tracks = []
    #     before_timestamp = None

    #     while len(all_tracks) < total_tracks:
    #         # Fetch a batch of recent tracks
    #         recent_tracks = self.get_recent_tracks(limit=batch_size, before=before_timestamp)
            
    #         if not recent_tracks['items']:
    #             # Exit if no more tracks are available
    #             break

    #         # Append fetched tracks to all_tracks
    #         all_tracks.extend(recent_tracks['items'])

    #         # Update the before_timestamp to the 'played_at' of the last track in this batch
    #         last_played_at = recent_tracks['items'][-1]['played_at']
    #         before_timestamp = int(datetime.fromisoformat(last_played_at.replace("Z", "+00:00")).timestamp() * 1000)

    #     # Limit to the specified number of tracks
    #     return all_tracks[:total_tracks]

    # def display_recent_tracks(self, total_tracks=200):
    #     recent_tracks = self.get_multiple_recent_tracks(total_tracks=total_tracks)

    #     print(f"\nMost Recent {len(recent_tracks)} Tracks Played:\n")
    #     for idx, item in enumerate(recent_tracks, 1):
    #         track = item['track']
    #         artist_name = track['artists'][0]['name']
    #         track_name = track['name']
    #         played_at = item['played_at']
    #         print(f"{idx}. {track_name} by {artist_name} (Played at: {played_at})")


# Instantiate SpotifyClient and fetch real-time top artists
spotify_client = SpotifyClient()
spotify_client.display_top_artist(5)
spotify_client.display_playlists(5)
spotify_client.display_top_tracks(5)
spotify_client.display_recent_tracks(50)

# test = spotify_client.sp.current_user_recently_played(limit=50, before=1735078561802)

# for idx, item in enumerate(test['items'], 1):
#     track = item['track']
#     artist_name = track['artists'][0]['name']
#     track_name = track['name']
#     played_at = item['played_at']
#     print(f"{idx}. {track_name} by {artist_name} (Played at: {played_at})")
