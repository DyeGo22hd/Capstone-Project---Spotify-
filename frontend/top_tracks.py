import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up authentication
client_credentials_manager = SpotifyClientCredentials(
    client_id='f3118b77a7154acb899ec1d17391c04c',
    client_secret='7797aa9c0c284fab822a42b3869449bf'
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Playlist ID
playlist_id = 'https://open.spotify.com/playlist/596GIcpIGocwj41T0zcn7d?si=KF7B6wZxQwukzZS-QH8GxQ'

# Get playlist tracks
results = sp.playlist_tracks(playlist_id)
tracks = results['items']

# Print track details
for idx, track in enumerate(tracks, 1):
    track_info = track['track']
    print(f"{idx}. {track_info['name']} - {track_info['artists'][0]['name']}")