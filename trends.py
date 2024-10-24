import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime

# Spotify API credentials
client_id = 'b24b1c78e21f447f8c7dce1d2a9d06c5'
client_secret = 'c83d6bbfcf884fc488c664d61600f81e'

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id="b24b1c78e21f447f8c7dce1d2a9d06c5", client_secret="c83d6bbfcf884fc488c664d61600f81e")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_artists(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    artists = []
    for item in results['items']:
        if item['track']:
            for artist in item['track']['artists']:
                artists.append({
                    'name': artist['name'],
                    'id': artist['id'],
                    'popularity': sp.artist(artist['id'])['popularity']
                })
    return artists

def get_trending_artists(limit=200):
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    playlists = [
        "37i9dQZEVXbLiRSasKsNU9",  # Viral 50 Global
        "37i9dQZEVXbMDoHDwVN2tF",  # Top 50 Global
        "37i9dQZF1DXcBWIGoYBM5M",  # Today's Top Hits
        "37i9dQZF1DX0XUsuxWHRQd",  # RapCaviar
        "37i9dQZF1DX10zKzsJ2jva",  # Teen Party
    ]
    
    all_artists = []
    for playlist in playlists:
        all_artists.extend(get_playlist_artists(playlist))
    
    # Remove duplicates and sort by popularity
    unique_artists = list({v['id']:v for v in all_artists}.values())
    sorted_artists = sorted(unique_artists, key=lambda x: x['popularity'], reverse=True)
    
    # Get the top 200 artists
    top_artists = sorted_artists[:limit]
    
    # Create a DataFrame
    df = pd.DataFrame(top_artists)
    df['rank'] = range(1, len(df) + 1)
    df = df[['rank', 'name', 'popularity', 'id']]
    
    # Save to CSV
    filename = f"trending_spotify_artists_{current_date}.csv"
    df.to_csv(filename, index=False)
    print(f"Trending artists saved to {filename}")
    
    return df

if __name__ == "__main__":
    trending_artists = get_trending_artists()
    
    # Display all 200 artists
    pd.set_option('display.max_rows', None)
    print(trending_artists)

    # Reset display options
    pd.reset_option('display.max_rows')
