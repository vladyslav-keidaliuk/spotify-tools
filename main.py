import config
from functions import (copy_favorite_tracks_to_public_playlist,
                       create_public_playlists_and_fill_from_favorite_by_100_tracks,
                       delete_prefix,
                       export_playlist_tracks_to_txt,
                       get_token_for_1_account,
                       get_token_for_2_account,
                       copy_from_1_to_2_account_all_favourite_tracks,
                       add_tracks_from_public_playlist_to_favorites,
                       remove_all_tracks_from_favorites,
                       remove_cache_files
                       )

# ====1====

# Need to give func a link in what public playlist you want copy a favorite playlist

# copy_favorite_tracks_to_public_playlist("LINK_ON_PUBLIC_PLAYLIST")


# ====2====

# Instead of 'Playlist' you can enter something else, as a result you will have playlists:
# Playlist 1, Playlist 2, Playlist 3......

# create_public_playlists_and_fill_from_favorite_by_100_tracks(config.root_account, "Playlist")



# ====3====

# Input your path to the folder in what you copied songs with prefix of service spotify-downloader.com
# Example of path :
# D:/SpotifySongs/

# delete_prefix("YOUR_PATH")

# ====4====

# Function that export names of tracks from public playlist to .txt file
# If 'is_sorted' - True -> titles will be sorting by ascending by alphabet
# If 'is_sorted' - False -> The track titles will be added in the same order as you have them in your playlist

# export_playlist_tracks_to_txt(
#     "LINK_ON_PUBLIC_PLAYLIST",
#     'test.txt',
#         True)

# ====5====

# To move all tracks in your favorites from account #1 to account #2 ,
# you need to do the following steps:
# Fill in the data:

account_1 = {
    "client_id": 'YOUR_CLIENT_ID',
    "client_secret": 'YOUR_CLIENT_SECRET',
    "redirect_uri": 'YOUR_REDIRECT_URI',
}

account_2 = {
    "client_id": 'YOUR_CLIENT_ID',
    "client_secret": 'YOUR_CLIENT_SECRET',
    "redirect_uri": 'YOUR_REDIRECT_URI',
}


# You need to log out of the account in the browser,
# execute the command to get the data of the account from which we will download tracks:

# get_token_for_1_account(account_1)

# You need to log out of the account in the browser,
# execute the command to get the data of the account to which we will upload tracks:

# get_token_for_2_account(account_2)

# Then you need to execute this function

# copy_from_1_to_2_account_all_favourite_tracks(account_1, account_2)



# ====6====

# ========================================================
# To add tracks from a public playlist to your favorites:
# add_tracks_from_public_playlist_to_favorites(
#     config.root_account,
#     "LINK_ON_PUBLIC_PLAYLIST")

# ========================================================


# ====7====
# !! DELETE ALL TRACKS
# remove_all_tracks_from_favorites(config.root_account)
#


# ====8====
# Deleted the cache
# remove_cache_files()