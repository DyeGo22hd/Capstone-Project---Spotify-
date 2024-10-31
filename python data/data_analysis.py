from spotify_client import SpotifyClient
from datetime import datetime, timedelta

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

        return artist_counts
    
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


    # def analyze_skipped_tracks(self, session_threshold=900):
    #     # Fetch recent tracks from Spotify
    #     recent_tracks = self.spotify_client.get_recent_tracks(limit=50)

    #     print("\nAnalysis of Recent Tracks for Skips (Using track duration):")
    #     skipped_tracks = []

    #     for idx in range(1, len(recent_tracks['items'])):
    #         # Access current and previous track details
    #         current_track = recent_tracks['items'][idx]['track']
    #         previous_track = recent_tracks['items'][idx - 1]['track']
    #         current_played_at = recent_tracks['items'][idx]['played_at']
    #         previous_played_at = recent_tracks['items'][idx - 1]['played_at']
            
    #         # Convert ISO strings to datetime objects
    #         current_played_datetime = datetime.fromisoformat(current_played_at.replace("Z", "+00:00"))
    #         previous_played_datetime = datetime.fromisoformat(previous_played_at.replace("Z", "+00:00"))
            
    #         # Check if both tracks were played on the same day and within the session threshold
    #         if (previous_played_datetime.date() == current_played_datetime.date() and
    #                 (current_played_datetime - previous_played_datetime).total_seconds() <= session_threshold):
                
    #             # Track duration
    #             track_duration_sec = previous_track['duration_ms'] / 1000  # Previous track duration in seconds

    #             # Determine if the track was "skipped" or "not skipped"
    #             # Here we assume that if it was played for less than 25% of the total duration, it is considered skipped
    #             played_duration = abs((current_played_datetime - previous_played_datetime).total_seconds())
    #             status = "Skipped" if played_duration < track_duration_sec * 0.25 else "Not Skipped"
                
    #             # Display the result for each track in the same session
    #             print(f"{idx}. {previous_track['name']} by {previous_track['artists'][0]['name']} - {status} "
    #                   f"(Played for approx. {int(played_duration)} seconds, "
    #                   f"Track Duration: {int(track_duration_sec)} seconds)")
                
    #             if status == "Skipped":
    #                 skipped_tracks.append({
    #                     "track_name": previous_track['name'],
    #                     "artist_name": previous_track['artists'][0]['name'],
    #                     "playback_duration": int(played_duration),
    #                     "track_duration": int(track_duration_sec)
    #                 })
                
    #         else:
    #             # If not in the same session, skip comparison
    #             print(f"{idx}. {previous_track['name']} by {previous_track['artists'][0]['name']} - Session ended, no skip analysis")
                
    #     return skipped_tracks


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

# Count the number of times each genre was listened to
genre_listen_counts = data_analysis.count_genre_listens(limit=50)

# Print the genre listen counts
print("\nGenre Listen Counts:")
for genre, count in genre_listen_counts.items():
    print(f"{genre}: {count} times")