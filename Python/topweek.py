import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('b24b1c78e21f447f8c7dce1d2a9d06c5'),
    client_secret=os.getenv('c83d6bbfcf884fc488c664d61600f81e')
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_top_artists():
    # Get the weekly global top artists chart
    playlist_id = '37i9dQZEVXbMDoHDwVN2tF'  # Global Top 50 playlist
    results = sp.playlist_tracks(playlist_id)
    
    # Create a dictionary to store artist frequencies
    artist_freq = {}
    
    # Count appearances of each artist
    for item in results['items']:
        track = item['track']
        for artist in track['artists']:
            name = artist['name']
            artist_freq[name] = artist_freq.get(name, 0) + 1
    
    # Sort artists by frequency
    sorted_artists = sorted(artist_freq.items(), key=lambda x: x[1], reverse=True)
    
    # Print top 10 artists
    print("\nTop Artists This Week:")
    print("----------------------")
    for i, (artist, count) in enumerate(sorted_artists[:10], 1):
        print(f"{i}. {artist} - {count} tracks")

if __name__ == "__main__":
    get_top_artists()
