import functions
from functions import (copy_favorite_tracks_to_public_playlist,
                       create_public_playlists_and_fill_from_favorite_by_100_tracks,
                       delete_prefix,
                       export_playlist_tracks_to_txt)

# ====1====

# Need to give func a link in what public playlist you want copy a favorite playlist

# copy_favorite_tracks_to_public_playlist("LINK_ON_PUBLIC_PLAYLIST")

# ====2====

# Instead of 'Playlist' you can enter something else, as a result you will have playlists:
# Playlist 1, Playlist 2, Playlist 3......

# create_public_playlists_and_fill_from_favorite_by_100_tracks("Playlist")

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
