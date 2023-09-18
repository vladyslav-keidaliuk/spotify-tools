import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import config

config.auth()


def get_playlist_uri_from_url(playlist_url):
    try:
        uri_start = playlist_url.index('playlist/') + len('playlist/')
        uri_end = playlist_url.index('?') if '?' in playlist_url else None
        return 'spotify:playlist:' + playlist_url[uri_start:uri_end]
    except Exception as e:
        print(f"Error at get_playlist_uri_from_url: {e}")


def copy_favorite_tracks_to_public_playlist(playlist_url):
    try:
        playlist_uri = get_playlist_uri_from_url(playlist_url)

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=config.CLIENT_ID,
                                      client_secret=config.CLIENT_SECRET,
                                      redirect_uri=config.REDIRECT_URI,
                                      scope='playlist-modify-public,user-library-read'))
        playlist = sp.playlist(playlist_uri)

        offset = 0
        limit = 50
        favorite_tracks = []
        while True:
            tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)['items']
            favorite_tracks.extend(tracks)
            if len(tracks) < limit:
                break
            offset += limit

        track_uris = [track['track']['uri'] for track in favorite_tracks]

        batch_size = 100
        track_uris_batches = [track_uris[i:i + batch_size] for i in range(0, len(track_uris), batch_size)]

        for batch in track_uris_batches:
            sp.playlist_add_items(playlist['id'], batch)

        print('All tracks successfully copy to public playlist!')
        sys.exit()
    except Exception as e:
        print(f"Error at copy_favorite_tracks_to_public_playlist: {e}")


def count_favorite_tracks():
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=config.CLIENT_ID,
                                      client_secret=config.CLIENT_SECRET,
                                      redirect_uri=config.REDIRECT_URI,
                                      scope='playlist-modify-public,user-library-read'))

        offset = 0
        limit = 50
        favorite_tracks = []
        print("Start counted.\nNeed to wait...")
        while True:
            tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)['items']
            favorite_tracks.extend(tracks)
            if len(tracks) < limit:
                break
            offset += limit
            print(f"Now in playlist: {len(favorite_tracks)}")

        return len(favorite_tracks)
    except Exception as e:
        print(f"Error at count_favorite_tracks: {e}")


def create_public_playlists_and_fill_from_favorite_by_100_tracks(prefix):
    try:

        num_playlists = int(int((count_favorite_tracks()) / 100) + 1)
        tracks_per_playlist = 100

        print("Started creating playlists...")

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=config.CLIENT_ID,
                                      client_secret=config.CLIENT_SECRET,
                                      redirect_uri=config.REDIRECT_URI,
                                      scope='playlist-modify-public,user-library-read'))
        offset = 0
        limit = 50
        favorite_tracks = []
        while True:
            tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)['items']
            favorite_tracks.extend(tracks)
            if len(tracks) < limit:
                break
            offset += limit

        track_uris = [track['track']['uri'] for track in favorite_tracks]

        for i in range(num_playlists):
            playlist_name = f'{prefix} {i + 1}'
            playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=True)
            playlist_id = playlist['id']

            start_index = i * tracks_per_playlist
            end_index = (i + 1) * tracks_per_playlist

            sp.playlist_add_items(playlist_id, track_uris[start_index:end_index])

        print('All tracks from the favorites were successfully separated and added to new playlists.')
    except Exception as e:
        print(f"Error at create_public_playlists_and_fill_from_favorite_by_100_tracks: {e}")


def delete_prefix(path):
    try:
        i = 0
        for filename in os.listdir(path):
            name = filename
            name = name[25:]
            my_dest = name + ".mp3"
            my_source = path + filename
            my_dest = path + my_dest
            os.rename(my_source, my_dest)
            i += 1

        print("All songs are renamed.")
    except Exception as e:
        print(f"Error: {e}")


def export_playlist_tracks_to_txt(playlist_url, output_file, is_sorted):
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=config.CLIENT_ID,
                                      client_secret=config.CLIENT_SECRET,
                                      redirect_uri=config.REDIRECT_URI,
                                      scope='playlist-read-private'))
        playlist_uri = get_playlist_uri_from_url(playlist_url)

        with open(output_file, 'w', encoding='utf-8') as file:
            offset = 0
            limit = 50
            while True:
                tracks = sp.playlist_tracks(playlist_uri, offset=offset, limit=limit)
                for track in tracks['items']:
                    track_name = track['track']['name']
                    file.write(f"{track_name}\n")
                if not tracks['next']:
                    break
                offset += limit

        if is_sorted is True:
            sort_playlist_tracks_in_file(output_file, output_file)
            print(f"The track names from the playlist have been successfully written"
                  f"to a file {output_file} and sorted by alphabet.")
        if is_sorted is False:
            print(f"The track names from the playlist have been successfully written to the file: {output_file}")

    except Exception as e:
        print(f"Error when exporting track names from a playlist: {e}")


def sort_playlist_tracks_in_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        sorted_lines = sorted(lines)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(sorted_lines)

        print(
            f"The track names from file '{input_file}' have been successfully"
            f" sorted and written to the file'{output_file}'.")
    except Exception as e:
        print(f"Error when sorting and recording tracks: {e}")

