import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config_helper

config = config_helper.get_data_from_config_files()

CLIENT_ID = config.get('CLIENT_ID')
CLIENT_SECRET = config.get('CLIENT_SECRET')
REDIRECT_URI = config.get('REDIRECT_URI')

def auth():
    try:
        client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp
    except Exception as e:
        print(f"Error : {e}")