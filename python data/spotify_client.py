import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from datetime import datetime
import zipfile
import json
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename


class SpotifyClient:
    def __init__(self):
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id="a1b69bc66206450b90556539dce74413",
                client_secret="fb50ad80e74840968e1e3047174a3ae2",
                redirect_uri="http://localhost:3000/callback",
                scope="user-top-read user-read-recently-played playlist-read-private playlist-modify-private playlist-modify-public"
            ))

            # Variables to store fetched data
            self.top_artists_data = None
            self.top_tracks_data = None
            self.playlists_data = None
            self.recent_tracks_data = None
            self.streaming_history_data = []


        except Exception as e:
            print(f"Error initializing Spotify client: {e}")

    # Fetch and store user top artists
    def fetch_top_artists(self, limit=5, time_range='long_term'):
        try:
            self.top_artists_data = self.sp.current_user_top_artists(limit=limit, time_range=time_range)
            print("Top artists data fetched successfully.")
        except Exception as e:
            print(f"Error fetching top artists: {e}")

    # Display stored top artists
    def display_top_artists(self):
        if not self.top_artists_data:
            print("No top artists data available. Fetch it first.")
            return

        print(f"\nTop Artists:\n")
        for idx, artist in enumerate(self.top_artists_data.get('items', []), 1):
            artist_name = artist['name']
            genres = ', '.join(artist.get('genres', []))
            print(f"{idx}. {artist_name} (Genres: {genres})")

    # Fetch and store user top tracks
    def fetch_top_tracks(self, limit=10, time_range="short_term"):
        try:
            self.top_tracks_data = self.sp.current_user_top_tracks(limit=limit, time_range=time_range)
            print("Top tracks data fetched successfully.")
        except Exception as e:
            print(f"Error fetching top tracks: {e}")

    # Display stored top tracks
    def display_top_tracks(self):
        if not self.top_tracks_data:
            print("No top tracks data available. Fetch it first.")
            return

        print(f"\nTop Tracks:\n")
        for idx, track in enumerate(self.top_tracks_data.get('items', []), 1):
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            print(f"{idx}. {track_name} by {artist_name}")

   
    # Fetch and store recent tracks
    def fetch_recent_tracks(self, limit=50):
        try:
            self.recent_tracks_data = self.sp.current_user_recently_played(limit=limit)
            print("Recent tracks data fetched successfully.")
        except Exception as e:
            print(f"Error fetching recent tracks: {e}")

    # Display stored recent tracks
    def display_recent_tracks(self):
        if not self.recent_tracks_data:
            print("No recent tracks data available. Fetch it first.")
            return

        print(f"\nMost Recent Tracks Played:\n")
        for idx, item in enumerate(self.recent_tracks_data.get('items', []), 1):
            track = item['track']
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            played_at = item['played_at']
            print(f"{idx}. {track_name} by {artist_name} (Played at: {played_at})")

    #Need to change this for the extended history and clean that data
    def extract_and_load_json(self):
            # Use Tkinter to open file dialog
        Tk().withdraw()  # Hide the root Tkinter window
        file_path = askopenfilename(
            title="Select your Spotify JSON file",
            filetypes=[("All Files", "*.*"), ("JSON Files", "*.json")]
        )

        if not file_path:
            print("No file selected.")
            return


        required_filename = "StreamingHistory_music_0.json"

        # Validate the filename
        if os.path.basename(file_path) != required_filename:
            print(f"Error: The uploaded file must be named '{required_filename}'.")
            return

        try:
            # Load the JSON data
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Ensure the data is sorted by the 'endTime' field (most recent last)
            data.sort(key=lambda x: datetime.strptime(x['endTime'], '%Y-%m-%d %H:%M'), reverse=True)

            # Store the data in the class attribute
            self.streaming_history_data = data
            print(f"Successfully loaded and sorted {len(data)} tracks from '{file_path}'.")

        except Exception as e:
            print(f"Error loading JSON file: {e}")

    def filter_tracks_by_date(self):
        """
        Filters and displays tracks from streaming history starting from the most recent
        till a user-specified month and year.

        Prompts the user for the target month and year.
        """
        if not self.streaming_history_data:
            print("No streaming history data available.")
            return

        # Ensure data is sorted by 'endTime' (most recent first)
        self.streaming_history_data.sort(
            key=lambda x: datetime.strptime(x['endTime'], '%Y-%m-%d %H:%M'), reverse=True
        )

        try:
            # Prompt the user for a month and year
            year = int(input("Enter the year (e.g., 2023): "))
            month = int(input("Enter the month (1-12): "))
            cutoff_date = datetime(year, month, 1)
        except ValueError:
            print("Invalid input. Please enter a valid year and month.")
            return

        print(f"\nShowing tracks from the most recent until {cutoff_date.strftime('%B %Y')}:\n")

        # Filter and display tracks
        for track in self.streaming_history_data:
            track_date = datetime.strptime(track['endTime'], '%Y-%m-%d %H:%M')

            # Stop if the track's date is earlier than the cutoff date
            if track_date < cutoff_date:
                break

            print(f"{track['trackName']} by {track['artistName']} (Played at: {track['endTime']})")

    # def save_recent_tracks_timeline(self, output_path="recent_tracks_timeline.png"):
    #     """
    #     Creates and saves a visually appealing timeline plot for recent track history using Plotly,
    #     with adjusted text positions to prevent overlap.

    #     :param output_path: Path where the timeline image will be saved.
    #     """
    #     if not self.recent_tracks_data or 'items' not in self.recent_tracks_data:
    #         print("No recent tracks data available.")
    #         return

    #     # Prepare data for the timeline
    #     timeline_data = []
    #     for idx, item in enumerate(self.recent_tracks_data['items']):
    #         track = item['track']
    #         played_at = datetime.strptime(item['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    #         track_name = track['name']
    #         artist_name = track['artists'][0]['name']

    #         # Alternate y-offsets for text placement
    #         offset = 1 if idx % 2 == 0 else -1

    #         timeline_data.append({
    #             "Played At": played_at,
    #             "Track Name": track_name,
    #             "Artist": artist_name,
    #             "Offset": offset
    #         })

    #     # Convert to DataFrame
    #     df = pd.DataFrame(timeline_data)

    #     # Create the Plotly timeline
    #     fig = go.Figure()

    #     # Add scatter trace for track points
    #     fig.add_trace(
    #         go.Scatter(
    #             x=df["Played At"],
    #             y=[1] * len(df),  # Fixed y-axis for timeline
    #             mode="markers",
    #             marker=dict(size=10, color="blue"),
    #             hovertemplate="<b>Track:</b> %{customdata[0]}<br><b>Played At:</b> %{x}<extra></extra>",
    #             name="Track Played",
    #             customdata=df[["Track Name", "Artist"]],  # Pass extra info for hover
    #         )
    #     )

    #     # Add a separate trace for text labels with offsets
    #     fig.add_trace(
    #         go.Scatter(
    #             x=df["Played At"],
    #             y=df["Offset"],  # Use offsets for alternate text placement
    #             mode="text",
    #             text=df["Track Name"],
    #             textposition="top center",
    #             hoverinfo="skip",  # Hide hover for text labels
    #             showlegend=False,  # No legend for text
    #         )
    #     )

    #     # Update layout for better readability
    #     fig.update_layout(
    #         title="Recent Track History Timeline",
    #         xaxis=dict(title="Date and Time Played", showgrid=True),
    #         yaxis=dict(title="", showticklabels=False),
    #         plot_bgcolor="white",
    #         height=500,
    #         margin=dict(l=50, r=50, t=50, b=50),
    #     )

    #     # Save the plot as an image
    #     fig.write_image(output_path)
    #     print(f"Timeline saved as {output_path}")

    


