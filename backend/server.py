from fastapi import FastAPI, UploadFile, Form
from spotify_client import SpotifyClient
from data_analysis import DataAnalysis
import json
import os

app = FastAPI()

# Instantiate Spotify client
spotify_client = SpotifyClient()

@app.post("/upload/")
async def upload_json(file: UploadFile, file_type: str = Form(...)):
    """
    Endpoint to upload JSON files for streaming or extended history.
    Saves the JSON data into the database for the current user.
    
    Args:
        file: The uploaded JSON file.
        file_type: The type of the file (e.g., 'streamingHistory', 'extendedHistory').
    """
    try:
        # Read the uploaded file content
        file_content = await file.read()
        file_path = f"/tmp/{file.filename}"

        # Save the content temporarily for processing
        with open(file_path, "wb") as temp_file:
            temp_file.write(file_content)

        # Process the JSON file with the Spotify client
        spotify_client.extract_and_load_json(file_path)

        # Remove the temporary file
        os.remove(file_path)

        return {"status": "success", "message": f"Uploaded {file_type} data successfully."}

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/filter_tracks/")
def filter_tracks(file_type: str, year: int, month: int):
    """
    Endpoint to filter tracks from JSON data by a specified year and month.
    
    Args:
        file_type: The type of data to filter ('streamingHistory' or 'extendedHistory').
        year: The year to filter from.
        month: The month to filter from.
    """
    try:
        tracks = spotify_client.filter_tracks_by_date(file_type, year, month)
        return {"filtered_tracks": tracks}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/top_artists/")
def get_top_artists(limit: int = 5, time_range: str = "short_term"):
    """
    Endpoint to fetch the user's top artists from Spotify.
    
    Args:
        limit: The number of top artists to fetch.
        time_range: The time range for fetching top artists (e.g., 'short_term', 'long_term').
    """
    try:
        top_artists = spotify_client.fetch_top_artists(limit=limit, time_range=time_range)
        return {"top_artists": top_artists}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/dynamic_playlist/")
def create_playlist(playlist_name: str = "Peepify Playlist", song_limit: int = 30):
    """
    Endpoint to generate a dynamic playlist based on the user's listening history.
    
    Args:
        playlist_name: The name of the playlist to create.
        song_limit: The maximum number of songs in the playlist.
    """
    try:
        from data_analysis import DataAnalysis
        data_analysis = DataAnalysis(spotify_client)

        data_analysis.dynamic_playlist(playlist_name, song_limit)
        return {"status": "success", "message": f"Playlist '{playlist_name}' created."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/recent_tracks/")
def get_recent_tracks(limit: int = 50):
    """
    Endpoint to fetch the user's recent tracks from Spotify.
    
    Args:
        limit: The number of recent tracks to fetch.
    """
    try:
        recent_tracks = spotify_client.fetch_recent_tracks(limit=limit)
        return {"recent_tracks": recent_tracks}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
