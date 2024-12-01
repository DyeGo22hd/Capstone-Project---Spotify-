from spotify_client import SpotifyClient
from data_analysis import DataAnalysis

def main():
    print("Initializing Spotify Client...\n")
    spotify_client = SpotifyClient()

    # Fetch and display top artists
    print("\nFetching top artists...")
    spotify_client.fetch_top_artists(limit=5)
    spotify_client.display_top_artists()

    # Fetch and display top tracks
    print("\nFetching top tracks...")
    spotify_client.fetch_top_tracks(limit=10)
    spotify_client.display_top_tracks()

    # Fetch and display recent tracks
    print("\nFetching recent tracks...")
    spotify_client.fetch_recent_tracks(limit=50)
    spotify_client.display_recent_tracks()

    # Load streaming history from JSON
    print("\nLoading streaming history data...")
    spotify_client.extract_and_load_json()

    # Prompt user for filtering date
    try:
        year = int(input("Enter the year to filter by (e.g., 2023): "))
        month = int(input("Enter the month to filter by (1-12): "))
    except ValueError:
        print("Invalid input. Please enter a valid month and year.")
        return

    # Initialize Data Analysis
    data_analysis = DataAnalysis(spotify_client)

    # Filter streaming history by the input date
    data_analysis.filter_streaming_history_by_date(month, year)

    # Display filtered streaming history
    print("\nDisplaying filtered streaming history...")
    data_analysis.display_filtered_streaming_history()

    # Analyze artist listen counts from filtered streaming history
    print("\nAnalyzing artist listen counts from filtered streaming history...")
    streaming_artist_counts = data_analysis.count_artist_listens_from_filtered_history()
    print("\nArtist Listen Counts (Filtered Streaming History):")
    for artist, count in streaming_artist_counts.items():
        print(f"{artist}: {count} times")


    # Analyze artist listen counts from recent tracks
    print("\nAnalyzing artist listen counts from recent tracks...")
    recent_artist_counts = data_analysis.count_artist_listens_from_recent_tracks(limit=50)
    print("\nArtist Listen Counts (Recent Tracks):")
    for artist, count in recent_artist_counts.items():
        print(f"{artist}: {count} times")

    print("\nCreating or updating dynamic playlist...")
    data_analysis.dynamic_playlist(playlist_name="Peepify Playlist", song_limit=30)

if __name__ == "__main__":
    main()
