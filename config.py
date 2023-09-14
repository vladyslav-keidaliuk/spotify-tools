import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8000/callback'

def auth():
    try:
        client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp
    except Exception as e:
        print(f"Error : {e}")