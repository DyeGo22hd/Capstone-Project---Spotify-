class DataAnalysis:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client

    def count_artist_listens_from_recent_tracks(self, limit=50):
        """
        Count the number of listens for each artist in the user's recent track history.
        """
        recent_tracks = self.spotify_client.fetch_recent_tracks(limit)
        artist_counts = {}

        if recent_tracks:
            for item in recent_tracks['items']:
                track = item['track']
                artist_name = track['artists'][0]['name']
                artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1

        return dict(sorted(artist_counts.items(), key=lambda item: item[1], reverse=True))

    def dynamic_playlist(self, playlist_name="Peepify Playlist", song_limit=30):
        """
        Create or update a playlist based on the top artists in the most recent track history.
        """
        sp = self.spotify_client.sp
        user_id = sp.current_user()['id']

        # Fetch and prioritize data
        recent_artist_counts = self.count_artist_listens_from_recent_tracks(limit=50)
        streaming_history = self.spotify_client.filter_tracks_by_date(file_type="streamingHistory")
        extended_history = self.spotify_client.filter_tracks_by_date(file_type="extendedHistory")

        artist_counts = {}
        for track in streaming_history:
            artist_name = track.get("artistName")
            if artist_name:
                artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1

        for track in extended_history:
            artist_name = track.get("master_metadata_album_artist_name")
            if artist_name:
                artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1

        sorted_artists = sorted({**recent_artist_counts, **artist_counts}.items(), key=lambda x: x[1], reverse=True)
        top_artists = [artist[0] for artist in sorted_artists[:5]]

        # Create or update playlist
        playlist_id = self.create_or_update_playlist(playlist_name)

        selected_tracks = []
        for artist in top_artists:
            artist_tracks = [
                track.get("spotify_track_uri") for track in streaming_history + extended_history
                if track.get("artistName" if track in streaming_history else "master_metadata_album_artist_name") == artist
            ]
            selected_tracks.extend(artist_tracks[:song_limit // len(top_artists)])

        sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks)
        print(f"Added {len(selected_tracks)} songs to the playlist '{playlist_name}'.")

    def create_or_update_playlist(self, playlist_name):
        """
        Create a new playlist or clear the existing one if it already exists.
        """
        sp = self.spotify_client.sp
        user_id = sp.current_user()['id']

        playlists = sp.current_user_playlists()
        playlist_id = None

        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                sp.user_playlist_replace_tracks(user_id, playlist_id, [])
                break

        if not playlist_id:
            playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
            playlist_id = playlist['id']

        return playlist_id
