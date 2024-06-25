import os
import sys
import time

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth

from tqdm import tqdm

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
        # First we delete all the tracks so we can re-record them later
        remove_all_tracks_from_your_public_playlist(playlist_url)

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

        total_tracks = count_favorite_tracks()

        with tqdm(total=total_tracks, desc="Fetching favorite tracks") as pbar:
            while True:
                tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)['items']
                favorite_tracks.extend(tracks)
                if len(tracks) < limit:
                    break
                offset += limit
                pbar.update(len(tracks))

        track_uris = [track['track']['uri'] for track in favorite_tracks]

        batch_size = 100
        track_uris_batches = tqdm([track_uris[i:i + batch_size] for i in range(0, len(track_uris), batch_size)])
        counter = 0

        for batch in track_uris_batches:
            sp.playlist_add_items(playlist['id'], batch)
            counter += int(len(batch))
            track_uris_batches.set_description("Filling the list with tracks ")

        print('All tracks successfully copy to public playlist!')
        sys.exit()
    except Exception as e:
        print(f"Error at copy_favorite_tracks_to_public_playlist: {e}")
    finally:
        remove_cache_files()


def remove_all_tracks_from_your_public_playlist(playlist_url):
    try:
        playlist_uri = get_playlist_uri_from_url(playlist_url)

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=config.CLIENT_ID,
                                      client_secret=config.CLIENT_SECRET,
                                      redirect_uri=config.REDIRECT_URI,
                                      scope='playlist-modify-public,user-library-read'))

        # Get a list of all tracks in the playlist
        playlist = sp.playlist(playlist_uri)
        total_tracks = playlist['tracks']['total']
        offset = 0
        limit = 100  # This is the maximum limit of tracks per request
        track_uris = []
        print("The deletion process for tracks in public playlist has begun >>")

        with tqdm(total=total_tracks + 100, desc="Collecting tracks for deleting ") as pbar:
            while offset < total_tracks:
                tracks = sp.playlist_tracks(playlist_uri, offset=offset, limit=limit)
                track_uris += [track['track']['uri'] for track in tracks['items']]
                offset += limit
                pbar.update(limit)
                pbar.set_postfix({"Deleted tracks": len(track_uris)})

        # Delete all tracks from the playlist
        with tqdm(total=len(track_uris) + 50, desc="Deleting: ") as pbar:
            for i in range(0, len(track_uris), 50):
                sp.playlist_remove_all_occurrences_of_items(playlist_uri, track_uris[i:i + 50])
                pbar.update(50)

        print('All tracks have been successfully removed from the playlist!')
    except Exception as e:
        print(f"There was an error: {str(e)}")


def count_favorite_tracks():
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=config.CLIENT_ID,
                                      client_secret=config.CLIENT_SECRET,
                                      redirect_uri=config.REDIRECT_URI,
                                      scope='playlist-modify-public,user-library-read'))

        total_tracks = int(sp.current_user_saved_tracks(limit=1)['total'])

        return total_tracks
    except Exception as e:
        print(f"Error at count_favorite_tracks: {e}")


def create_public_playlists_and_fill_from_favorite_by_100_tracks(account, prefix):
    try:

        print("Started creating playlists...")

        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(client_id=account['client_id'],
                                      client_secret=account['client_secret'],
                                      redirect_uri=config.REDIRECT_URI,
                                      scope='playlist-modify-public,user-library-read'))

        total_tracks = int(sp.current_user_saved_tracks(limit=1)['total'])
        num_playlists = int((total_tracks / 100) + 1)
        tracks_per_playlist = 100

        offset = 0
        limit = 50
        favorite_tracks = []

        with tqdm(total=total_tracks, desc="Fetching favorite tracks") as pbar:
            while True:
                tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)['items']
                favorite_tracks.extend(tracks)
                if len(tracks) < limit:
                    break
                offset += limit
                pbar.update(int(len(tracks)))

        track_uris = [track['track']['uri'] for track in favorite_tracks]

        for i in tqdm(range(num_playlists), desc="Creating playlists and inserting tracks"):
            playlist_name = f'{prefix} {i + 1}'
            playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=True)
            playlist_id = playlist['id']

            start_index = i * tracks_per_playlist
            end_index = (i + 1) * tracks_per_playlist

            sp.playlist_add_items(playlist_id, track_uris[start_index:end_index])

        print('All tracks from the favorites were successfully separated and added to new playlists.')
    except Exception as e:
        print(f"Error at create_public_playlists_and_fill_from_favorite_by_100_tracks: {e}")
    finally:
        remove_cache_files()


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
    finally:
        remove_cache_files()


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


def get_token_for_1_account(account_1):
    try:
        cache_path_first_account = ".cache-first_account"
        util.prompt_for_user_token(
            scope='user-library-read user-library-modify',
            client_id=account_1['client_id'],
            client_secret=account_1['client_secret'],
            redirect_uri=account_1['redirect_uri'],
            cache_path=cache_path_first_account
        )
    except Exception as e:
        print(f"Error in get_token_for_1_account: {e}")


def get_token_for_2_account(account_2):
    try:
        cache_path_second_account = ".cache-second_account"

        util.prompt_for_user_token(
            scope='user-library-read user-library-modify',
            client_id=account_2['client_id'],
            client_secret=account_2['client_secret'],
            redirect_uri=account_2['redirect_uri'],
            cache_path=cache_path_second_account
        )
    except Exception as e:
        print(f"Error in get_token_for_2_account: {e}")


def copy_from_1_to_2_account_all_favourite_tracks(account_1, account_2):
    try:

        sp_oauth_first_account = SpotifyOAuth(
            client_id=account_1['client_id'],
            client_secret=account_1['client_secret'],
            redirect_uri=account_1['redirect_uri'],
            scope='user-library-read user-library-modify',
            cache_path=".cache-first_account"  # The path to the cache file for the first account
        )

        # Get an access token for your first account
        token_first_account = sp_oauth_first_account.get_access_token()
        if token_first_account:
            sp_first_account = spotipy.Spotify(auth=token_first_account['access_token'])

            # Initialize the SpotifyOAuth object for the second account
            sp_oauth_second_account = SpotifyOAuth(
                client_id=account_2['client_id'],
                client_secret=account_2['client_secret'],
                redirect_uri=account_2['redirect_uri'],
                scope='user-library-read user-library-modify',
                cache_path=".cache-second_account"  # The path to the cache file for the second account
            )

            # Get an access token for the second account
            token_second_account = sp_oauth_second_account.get_access_token()
            if token_second_account:
                sp_second_account = spotipy.Spotify(auth=token_second_account['access_token'])

                # Get tracks from the first account's saved tracks
                offset = 0
                limit = 50  # API limit is 50 tracks per request
                first_account_tracks = []
                total_tracks = int(sp_first_account.current_user_saved_tracks(limit=1)['total'])

                print("Started copying tracks from the favorite first account >>")
                with tqdm(total=total_tracks, desc="Copying tracks") as pbar:
                    while True:
                        tracks_batch = sp_first_account.current_user_saved_tracks(limit=limit, offset=offset)
                        if not tracks_batch['items']:
                            break
                        first_account_tracks.extend(tracks_batch['items'])
                        offset += limit
                        pbar.update(len(tracks_batch['items']))

                print("\nStarted inserting tracks into the favorites of the 2nd account >>")
                with tqdm(total=len(first_account_tracks), desc="Inserting tracks") as pbar:
                    counter = 0
                    for item in reversed(first_account_tracks):
                        track_id = item['track']['id']
                        try:
                            sp_second_account.current_user_saved_tracks_add(tracks=[track_id])
                            counter += 1
                            time.sleep(1)
                            pbar.update(1)
                        except Exception as e:
                            print(f"Error occurred while adding track with id {track_id}: {str(e)}")

                print("All tracks successfully added to favorites on the second account.")
            else:
                print("Failed to get access token for the second account.")
        else:
            print("Failed to get access token for the first account.")
    except Exception as e:
        print(f"Error at copy_from_1_to_2_account_saved_tracks_all: {e}")
    finally:
        remove_cache_files()



def add_tracks_from_public_playlist_to_favorites(account, playlist_url):
    try:
        playlist_uri = get_playlist_uri_from_url(playlist_url)

        sp_second_account = SpotifyOAuth(
            client_id=account['client_id'],
            client_secret=account['client_secret'],
            redirect_uri=config.REDIRECT_URI,
            scope='user-library-read user-library-modify playlist-modify-public',
            cache_path=".cache"
        )

        token_second_account = sp_second_account.get_access_token()
        if token_second_account:
            global sp
            sp = spotipy.Spotify(auth=token_second_account['access_token'])


        playlist = sp.playlist_tracks(playlist_uri, additional_types=('track',))
        total_tracks = playlist['total']
        print(total_tracks)

        offset = 0
        limit = 50
        favorite_tracks = []
        count = []

        with tqdm(total=total_tracks, desc="Fetching tracks from public playlist") as pbar:
            while True:
                tracks = sp.playlist_items(playlist_uri, offset=offset, limit=limit)['items']
                favorite_tracks.extend(tracks)
                count += tracks
                if len(tracks) < limit:
                    break
                offset += limit
                pbar.update(limit)

        track_uris = [track['track']['uri'] for track in reversed(favorite_tracks)]
        batch_size = 1  # This should be so that the track ORDER IS PRESERVED

        track_uris_batches = [track_uris[i:i + batch_size] for i in range(0, len(track_uris), batch_size)]

        tracks_baches = []
        for batch in track_uris_batches:
            tracks_baches.append(batch)

        tracks_baches = tqdm(tracks_baches)
        for batch1 in tracks_baches:
            sp.current_user_saved_tracks_add(batch1)
            time.sleep(1)
            tracks_baches.set_description("Inserting tracks into favorites")

        print('All tracks successfully added to favorites!')
    except Exception as e:
        print(f"Error at add_tracks_from_public_playlist_to_favorites: {e}")
    finally:
        remove_cache_files()


def remove_all_tracks_from_favorites(account):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=account['client_id'],
            client_secret=account['client_secret'],
            redirect_uri=config.REDIRECT_URI,
            scope='user-library-read user-library-modify',
            cache_path=".cache"

        ))

        favorite_tracks = sp.current_user_saved_tracks(limit=50)['items']
        total_tracks = sp.current_user_saved_tracks()['total']

        with tqdm(total=total_tracks, desc="Deleting tracks from favorite") as pbar:
            while favorite_tracks:
                track_uris = [track['track']['uri'] for track in favorite_tracks]
                sp.current_user_saved_tracks_delete(tracks=track_uris)
                favorite_tracks = sp.current_user_saved_tracks(limit=50)['items']
                pbar.update(50)
        print(f'All {total_tracks} tracks successfully removed from favorites!')
        remove_cache_files()
    except Exception as e:
        print(f"Error at remove_all_tracks_from_favorites: {e}")


def remove_cache_files():
    try:
        cache_files = [".cache", ".cache-first_account", ".cache-second_account"]

        for file in cache_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"The {file} file has been successfully deleted.")
            else:
                print(f"The file {file} does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting files:{str(e)}")
