import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from datetime import datetime

# Spotify API credentials
client_id = 'f3118b77a7154acb899ec1d17391c04c'
client_secret = '7797aa9c0c284fab822a42b3869449bf'

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_trending_artists(limit=200):
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Search for top tracks
    search_queries = ['pop', 'rap', 'rock', 'hip hop', 'top']
    all_artists = []
    
    for query in search_queries:
        results = sp.search(q=query, type='track', limit=50)
        for track in results['tracks']['items']:
            for artist in track['artists']:
                all_artists.append({
                    'name': artist['name'],
                    'id': artist['id'],
                    'popularity': sp.artist(artist['id'])['popularity']
                })
    
    # Remove duplicates and sort by popularity
    unique_artists = list({v['id']:v for v in all_artists}.values())
    sorted_artists = sorted(unique_artists, key=lambda x: x['popularity'], reverse=True)
    
    # Get the top artists
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
    pd.set_option('display.max_rows', None)
    print(trending_artists)
    pd.reset_option('display.max_rows')
