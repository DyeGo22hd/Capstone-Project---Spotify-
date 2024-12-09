import json
import os
import pymysql
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
import spotipy


class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="b24b1c78e21f447f8c7dce1d2a9d06c5",
            client_secret="c83d6bbfcf884fc488c664d61600f81e",
            redirect_uri="https://cloud.appwrite.io/v1/account/sessions/oauth2/callback/spotify/66f9aeb700248be20f22",
            scope="user-top-read user-read-recently-played"
        ))
        self.db_config = {
            "host": "peepify-db.c7swoaco2oxs.us-east-2.rds.amazonaws.com",
            "port": 3306,
            "user": "peepify",
            "password": "capstone499",
            "database": "peepify_data"
        }

    def fetch_top_artists(self, limit=5, time_range="short_term"):
        """
        Fetch the user's top artists from Spotify.
        """
        try:
            return self.sp.current_user_top_artists(limit=limit, time_range=time_range)
        except Exception as e:
            print(f"Error fetching top artists: {e}")
            return None

    def fetch_recent_tracks(self, limit=50):
        """
        Fetch the user's recent tracks from Spotify.
        """
        try:
            return self.sp.current_user_recently_played(limit=limit)
        except Exception as e:
            print(f"Error fetching recent tracks: {e}")
            return None

    def extract_and_load_json(self, file_path):
        """
        Extract data from a JSON file and save it to the database for the current user.
        Supports both StreamingHistory and ExtendedHistory file types.
        """
        file_name = os.path.basename(file_path)
        user_id = self.sp.current_user()['id']

        # Connect to the database
        connection = pymysql.connect(**self.db_config)

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            with connection.cursor() as cursor:
                # Check if the user exists
                cursor.execute("SELECT * FROM user_info WHERE current_user_id = %s", (user_id,))
                user = cursor.fetchone()

                if not user:
                    # Insert new user
                    cursor.execute(
                        "INSERT INTO user_info (current_user_id, raw_data_id, api_data_id) VALUES (%s, NULL, NULL)",
                        (user_id,)
                    )
                    connection.commit()
                    print(f"New user '{user_id}' created in the database.")

                # Determine the type of JSON and update the appropriate field
                if "Streaming_History_Audio" in file_name:
                    cursor.execute(
                        """
                        INSERT INTO raw_data (raw_data_id, extended_id)
                        VALUES ((SELECT raw_data_id FROM user_info WHERE current_user_id = %s), %s)
                        ON DUPLICATE KEY UPDATE extended_id = VALUES(extended_id);
                        """,
                        (user_id, json.dumps(data))
                    )
                elif "StreamingHistory_music" in file_name:
                    cursor.execute(
                        """
                        INSERT INTO raw_data (raw_data_id, streaming_history_id)
                        VALUES ((SELECT raw_data_id FROM user_info WHERE current_user_id = %s), %s)
                        ON DUPLICATE KEY UPDATE streaming_history_id = VALUES(streaming_history_id);
                        """,
                        (user_id, json.dumps(data))
                    )

                connection.commit()
                print(f"JSON data from '{file_name}' successfully saved to the database for user '{user_id}'.")

        except Exception as e:
            print(f"Error processing file '{file_name}': {e}")

        finally:
            connection.close()

    def filter_tracks_by_date(self, file_type="streamingHistory", year=2024, month=1):
        """
        Filter tracks from the database based on a specified year and month.
        Supports both StreamingHistory and ExtendedHistory data.
        """
        connection = pymysql.connect(**self.db_config)
        user_id = self.sp.current_user()['id']

        try:
            with connection.cursor() as cursor:
                if file_type == "streamingHistory":
                    cursor.execute(
                        "SELECT streaming_history_json FROM raw_data WHERE raw_data_id = (SELECT raw_data_id FROM user_info WHERE current_user_id = %s)",
                        (user_id,)
                    )
                elif file_type == "extendedHistory":
                    cursor.execute(
                        "SELECT extended_history_json FROM raw_data WHERE raw_data_id = (SELECT raw_data_id FROM user_info WHERE current_user_id = %s)",
                        (user_id,)
                    )
                result = cursor.fetchone()

                if result:
                    json_data = json.loads(result[0])
                    cutoff_date = datetime(year, month, 1)

                    filtered_tracks = [
                        track for track in json_data
                        if datetime.strptime(track.get("endTime" if file_type == "streamingHistory" else "ts"),
                                             "%Y-%m-%d %H:%M" if file_type == "streamingHistory" else "%Y-%m-%dT%H:%M:%SZ") >= cutoff_date
                    ]
                    return filtered_tracks
                else:
                    print(f"No data available for {file_type}.")
                    return []

        except Exception as e:
            print(f"Error filtering tracks: {e}")
            return []

        finally:
            connection.close()
