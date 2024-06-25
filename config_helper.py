import json
import os


def get_value_from_json(json_file, key):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data.get(key)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error while reading JSON file: {e}")
        return None


def get_config_value(json_file, key):
    value = get_value_from_json(json_file, key)

    if not value:
        value = os.getenv(key)

    return value


def get_data_from_config_files():
    json_file = 'config.json'
    keys = ['SpotifyToolsClientID', 'SpotifyToolsClientSecret', 'SpotifyToolsRedirectURI']
    config_values = {key: get_config_value(json_file, key) for key in keys}

    switcher = {
        'SpotifyToolsClientID': 'CLIENT_ID',
        'SpotifyToolsClientSecret': 'CLIENT_SECRET',
        'SpotifyToolsRedirectURI': 'REDIRECT_URI'
    }

    return {switcher[key]: value for key, value in config_values.items() if value}
