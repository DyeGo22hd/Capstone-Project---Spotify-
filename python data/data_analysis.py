from spotify_client import SpotifyClient
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class DataAnalysis:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client

    def count_artist_listens(self, limit=50):
        # Retrieve recent tracks
        recent_tracks = self.spotify_client.get_recent_tracks(limit)

        artist_counts = {}

        # Iterate through the recent tracks
        for item in recent_tracks['items']:
            track = item['track']
            artist_name = track['artists'][0]['name']

            # Update the artist count
            artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1

        # Sort artist_counts dictionary by listen counts in descending order
        sorted_artist_counts = dict(sorted(artist_counts.items(), key=lambda item: item[1], reverse=True))

        return sorted_artist_counts
    
    def count_artist_listens_from_streaming_history(self, limit=50):

        # Ensure streaming history data exists
        if not hasattr(self.spotify_client, 'streaming_history_data'):
            print("No streaming history data available.")
            return {}

        # Limit the records processed
        streaming_history = self.spotify_client.streaming_history_data[-limit:][::-1]

        artist_counts = {}

        # Count artist listens in the streaming history
        for record in streaming_history:
            artist_name = record.get("artistName", "Unknown Artist")
            artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1

        # Sort artist_counts dictionary by listen counts in descending order
        sorted_artist_counts = dict(sorted(artist_counts.items(), key=lambda item: item[1], reverse=True))

        return sorted_artist_counts
    

    
    def count_genre_listens(self, limit=50):
        # Retrieve recent tracks
        recent_tracks = self.spotify_client.get_recent_tracks(limit)

        genre_counts = {}

        # Iterate through the recent tracks
        for item in recent_tracks['items']:
            track = item['track']
            artist_name = track['artists'][0]['name']
            
            # Fetch genres for the artist
            artist_info = self.spotify_client.sp.artist(track['artists'][0]['id'])
            genres = artist_info['genres']

            # Update the genre count for each genre associated with the artist
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

        return genre_counts



# Usage Example:
spotify_client = SpotifyClient()
data_analysis = DataAnalysis(spotify_client)
# skipped_tracks = data_analyzer.analyze_skipped_tracks(session_threshold=900)

# Count the number of times each artist was listened to
artist_listen_counts = data_analysis.count_artist_listens(limit=50)

# Print the results
print("\nArtist Listen Counts:")
for artist, count in artist_listen_counts.items():
    print(f"{artist}: {count} times")

print()
spotify_client.extract_and_load_json("C:/Users/tinci/Downloads/my_spotify_data.zip",'my_spotify_data.zip')
streamed_artist_listen_counts = data_analysis.count_artist_listens_from_streaming_history(limit=250)
print()

print("\nArtist Listen Counts from Streaming History:")
for artist, count in streamed_artist_listen_counts.items():
    print(f"{artist}: {count} times")

# Count the number of times each genre was listened to
genre_listen_counts = data_analysis.count_genre_listens(limit=50)

# Print the genre listen counts
print("\nGenre Listen Counts:")
for genre, count in genre_listen_counts.items():
    print(f"{genre}: {count} times")