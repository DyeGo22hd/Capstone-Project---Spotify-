import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from datetime import datetime
import zipfile
import json
import os
import matplotlib.pyplot as plt


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

    def extract_and_load_json(self, zip_path, output_folder="extracted_data"):
        # Ensure the output directory exists
        os.makedirs(output_folder, exist_ok=True)
        
        # Open the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Define the target JSON files and their corresponding attributes
            target_files = {
                "Spotify Account Data/Marquee.json": "marquee_data",
                "Spotify Account Data/SearchQueries.json": "search_queries_data",
                "Spotify Account Data/StreamingHistory_music_0.json": "streaming_history_data"
            }

            for file, attribute_name in target_files.items():
                if file in zip_ref.namelist():
                    # Extract and load JSON data from each file
                    with zip_ref.open(file) as f:
                        file_data = json.load(f)
                        setattr(self, attribute_name, file_data)
                        print(f"Loaded data from {file}")

                    # Save the JSON content to the output folder
                    base_name = os.path.basename(file)
                    output_path = os.path.join(output_folder, base_name)
                    with open(output_path, 'w') as output_file:
                        json.dump(file_data, output_file)
                        print(f"Data saved to {output_path}")

    def display_streaming_history(self, limit=50):
        
        if not self.streaming_history_data:
            print("No streaming history data available.")
            return

        # Enforce a maximum limit of 200
        limit = min(limit, 250)

        # Reverse the streaming history to show the most recent tracks first
        recent_tracks = self.streaming_history_data[-limit:][::-1]

        print(f"\nMost Recent {limit} Tracks Played:\n")
        for idx, record in enumerate(recent_tracks, 1):
            end_time = record.get("endTime", "N/A")
            artist_name = record.get("artistName", "Unknown Artist")
            track_name = record.get("trackName", "Unknown Track")
            ms_played = record.get("msPlayed", 0)
            seconds_played = ms_played // 1000

            print(f"{idx}. {track_name} by {artist_name} (End Time: {end_time}, Duration: {seconds_played} seconds)")

    def plot_recent_tracks_timeline(self, limit=50):
            """Plots a timeline of the recently played tracks."""
            recent_tracks = self.get_recent_tracks(limit)['items']
            played_times = []
            track_names = []

            for item in recent_tracks:
                played_at = item['played_at']
                track_name = item['track']['name']
                played_times.append(datetime.fromisoformat(played_at[:-1]))  # Convert to datetime
                track_names.append(track_name)

            plt.figure(figsize=(12, 6))
            plt.plot(played_times, range(len(played_times)), marker='o', linestyle='-', color='b')
            plt.yticks(range(len(track_names)), track_names)
            plt.title(f'Timeline of Recently Played Tracks (Last {limit} Tracks)')
            plt.xlabel('Time Played')
            plt.ylabel('Tracks')
            plt.xticks(rotation=45)
            plt.grid()
            plt.tight_layout()
            plt.show()

    def plot_streaming_history_timeline(self, limit=50):
        """Plots a timeline of the streaming history."""
        if not self.streaming_history_data:
            print("No streaming history data available.")
            return

        # Enforce a maximum limit
        limit = min(limit, len(self.streaming_history_data))
        recent_history = self.streaming_history_data[-limit:]
        played_times = []
        track_names = []

        for record in recent_history:
            end_time = record.get("endTime")
            track_name = record.get("trackName", "Unknown Track")
            played_times.append(datetime.fromisoformat(end_time[:-1]))  # Convert to datetime
            track_names.append(track_name)

        plt.figure(figsize=(12, 6))
        plt.plot(played_times, range(len(played_times)), marker='o', linestyle='-', color='g')
        plt.yticks(range(len(track_names)), track_names)
        plt.title(f'Timeline of Streaming History (Last {limit} Tracks)')
        plt.xlabel('Time Played')
        plt.ylabel('Tracks')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.show()


# Instantiate SpotifyClient and fetch real-time top artists
spotify_client = SpotifyClient()
spotify_client.display_top_artist(5)
spotify_client.display_playlists(5)
spotify_client.display_top_tracks(5)
spotify_client.display_recent_tracks(50)

print()
#Open and Fetch data from Zip
spotify_client.extract_and_load_json("C:/Users/tinci/Downloads/my_spotify_data.zip",'my_spotify_data.zip')

# Access the loaded data for each JSON file
# print("Marquee Data:", spotify_client.marquee_data)
# print("Search Queries Data:", spotify_client.search_queries_data)
# print("Streaming History Data:", spotify_client.streaming_history_data)
spotify_client.display_streaming_history(250)

spotify_client.plot_recent_tracks_timeline(limit=50)
# spotify_client.plot_streaming_history_timeline(limit=250)
