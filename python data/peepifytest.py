import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up your credentials
client_id = 'b24b1c78e21f447f8c7dce1d2a9d06c5'
client_secret = 'c83d6bbfcf884fc488c664d61600f81e'

# Authenticate using SpotifyClientCredentials
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_top_tracks_from_playlist(playlist_id):
    # Fetch the tracks from a specific playlist (e.g., Top 50 Global)
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Collect artist info from the tracks
    artist_popularity = {}
    
    for track in tracks:
        artist = track['track']['artists'][0]
        artist_id = artist['id']
        artist_data = sp.artist(artist_id)
        artist_name = artist_data['name']
        popularity = artist_data['popularity']

        # Store artist popularity in a dictionary
        artist_popularity[artist_name] = popularity
    
    return artist_popularity

def find_second_most_popular_artist(artist_popularity):
    # Sort artists by popularity in descending order
    sorted_artists = sorted(artist_popularity.items(), key=lambda x: x[1], reverse=True)
    
    if len(sorted_artists) >= 2:
        return sorted_artists[1]  # Return the second most popular artist
    return None

# Define the playlist ID for "Top 50 Global"
playlist_id = '37i9dQZEVXbMDoHDwVN2tF'  # Spotify Global Top 50

# Get artist popularity from the playlist
artist_popularity = get_top_tracks_from_playlist(playlist_id)

if artist_popularity:
    print("Top Artists from Global Playlist:")
    for artist, popularity in artist_popularity.items():
        print(f"{artist} - Popularity: {popularity}")
    
    # Find the second most popular artist
    second_most_popular_artist = find_second_most_popular_artist(artist_popularity)
    
    if second_most_popular_artist:
        print("\nSecond Most Popular Artist:")
        print(f"Artist: {second_most_popular_artist[0]}")
        print(f"Popularity: {second_most_popular_artist[1]}")
    else:
        print("\nNot enough data to determine the second most popular artist.")
else:
    print("No artist data found.")

def find_least_popular_artist(artist_popularity):
    # Find the artist with the least popularity
    least_popular_artist = min(artist_popularity.items(), key=lambda x: x[1])
    return least_popular_artist

# Define the playlist ID for "Top 50 Global"
playlist_id = '37i9dQZEVXbMDoHDwVN2tF'  # Spotify Global Top 50

# Get artist popularity from the playlist
artist_popularity = get_top_tracks_from_playlist(playlist_id)

if artist_popularity:
    print("Top Artists from Global Playlist:")
    for artist, popularity in artist_popularity.items():
        print(f"{artist} - Popularity: {popularity}")
    
    # Find the least popular artist
    least_popular_artist = find_least_popular_artist(artist_popularity)
    
    if least_popular_artist:
        print("\nLeast Popular Artist:")
        print(f"Artist: {least_popular_artist[0]}")
        print(f"Popularity: {least_popular_artist[1]}")
else:
    print("No artist data found.")