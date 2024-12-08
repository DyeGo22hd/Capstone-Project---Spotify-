from datetime import datetime


class DataAnalysis:
    def __init__(self, spotify_client):
        """
        Initialize the DataAnalysis class with a SpotifyClient instance.

        :param spotify_client: Instance of SpotifyClient to access Spotify data.
        """
        self.spotify_client = spotify_client
        self.filtered_streaming_data = []

    def filter_streaming_history_by_date(self, month, year):
        """
        Filters streaming history data from the most recent entry to the specified month and year.

        :param month: The target month (1-12).
        :param year: The target year.
        """
        if not self.spotify_client.streaming_history_data:
            print("No streaming history data available.")
            return

        cutoff_date = datetime(year, month, 1)
        print(f"\nFiltering streaming history from the most recent until {cutoff_date.strftime('%B %Y')}...\n")

        self.filtered_streaming_data = [
            track for track in self.spotify_client.streaming_history_data
            if datetime.strptime(track['endTime'], '%Y-%m-%d %H:%M') >= cutoff_date
        ]

        print(f"Filtered {len(self.filtered_streaming_data)} tracks.")

    def count_artist_listens_from_filtered_history(self):
        """
        Count the number of times each artist was listened to in the filtered streaming history.

        :return: Dictionary of artist names and their listen counts.
        """
        if not self.filtered_streaming_data:
            print("No filtered streaming history data available.")
            return {}

        artist_counts = {}

        for record in self.filtered_streaming_data:
            artist_name = record.get("artistName", "Unknown Artist")
            artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1

        return dict(sorted(artist_counts.items(), key=lambda x: x[1], reverse=True))

   
    def display_filtered_streaming_history(self):
        """
        Displays the filtered streaming history tracks.

        :return: None
        """
        if not self.filtered_streaming_data:
            print("No filtered streaming history data available.")
            return

        print("\nFiltered Streaming History:")
        for track in self.filtered_streaming_data:
            print(f"{track['trackName']} by {track['artistName']} (Played at: {track['endTime']})")

    def count_artist_listens_from_recent_tracks(self, limit=50):

        """
        Count the number of times each artist was listened to in the recent tracks data.

        :param limit: Number of tracks to analyze from recent tracks.
        :return: Dictionary of artist names and their listen counts.
        """
        if not self.spotify_client.recent_tracks_data or 'items' not in self.spotify_client.recent_tracks_data:
            print("No recent tracks data available.")
            return {}

        recent_tracks = self.spotify_client.recent_tracks_data['items'][:limit]
        artist_counts = {}

        for item in recent_tracks:
            artist_name = item['track']['artists'][0]['name']
            artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1

        return dict(sorted(artist_counts.items(), key=lambda x: x[1], reverse=True))
    
    def dynamic_playlist(self, playlist_name="Peepify Playlist", song_limit=30):
        """
        Create or update a playlist based on the top artists in the recent track history.
        The playlist will only include songs from the recent track history and the user's
        streaming history, prioritizing the most listened-to songs by the user.

        :param playlist_name: Name of the playlist to create or update.
        :param song_limit: Maximum number of songs in the playlist.
        """
        sp = self.spotify_client.sp  # Spotify client
        user_id = sp.current_user()['id']

        # Step 1: Check if the playlist exists
        try:
            playlists = sp.current_user_playlists(limit=50)
            playlist_items = playlists.get('items', [])
            if not isinstance(playlist_items, list):
                playlist_items = []
        except Exception as e:
            print(f"Error fetching playlists: {e}")
            return

        # Search for the playlist
        playlist_id = None
        for playlist in playlist_items:
            if isinstance(playlist, dict) and playlist.get('name') == playlist_name:
                playlist_id = playlist.get('id')
                break

        # Step 2: Create the playlist if it doesn't exist
        if not playlist_id:
            try:
                playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description="Generated by Peepify")
                playlist_id = playlist['id']
                print(f"Created playlist '{playlist_name}'.")
            except Exception as e:
                print(f"Error creating playlist '{playlist_name}': {e}")
                return
        else:
            # Step 3: Clear the existing playlist
            try:
                sp.user_playlist_replace_tracks(user_id, playlist_id, [])
                print(f"Cleared playlist '{playlist_name}'.")
            except Exception as e:
                print(f"Error clearing playlist '{playlist_name}': {e}")
                return

        # Step 4: Analyze recent tracks and calculate artist proportions
        recent_artist_counts = self.count_artist_listens_from_recent_tracks(limit=50)
        total_recent_listens = sum(recent_artist_counts.values())
        artist_proportions = {
            artist: count / total_recent_listens for artist, count in recent_artist_counts.items()
        }

        # Step 5: Collect songs for the playlist
        selected_tracks = []
        added_tracks = set()  # To avoid duplicates

        for artist, proportion in artist_proportions.items():
            if len(selected_tracks) >= song_limit:
                break

            # Calculate the number of songs to include for this artist
            artist_song_limit = round(proportion * song_limit)

            # Get songs from recent tracks
            recent_tracks = [
                track['track']['uri'] for track in self.spotify_client.recent_tracks_data['items']
                if track['track']['artists'][0]['name'] == artist
            ]

            # Get songs from streaming history (match by trackName and artistName)
            streaming_tracks = [
                self.spotify_client.sp.search(
                    q=f"track:{track['trackName']} artist:{track['artistName']}",
                    type="track",
                    limit=1
                )['tracks']['items'][0]['uri']
                for track in self.filtered_streaming_data
                if track.get('artistName') == artist and 'trackName' in track
            ]

            # Combine tracks, prioritizing recent tracks first
            all_tracks = recent_tracks + streaming_tracks

            for track_uri in all_tracks:
                if len(selected_tracks) >= song_limit:
                    break
                if track_uri not in added_tracks:
                    selected_tracks.append(track_uri)
                    added_tracks.add(track_uri)

        # Step 6: Add selected tracks to the playlist
        try:
            sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks)
            print(f"Added {len(selected_tracks)} songs to playlist '{playlist_name}'.")
        except Exception as e:
            print(f"Error adding tracks to playlist: {e}")
