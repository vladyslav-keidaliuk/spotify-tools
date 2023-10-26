# spotify-tools

I've created a set of features to help you do things that can't be done
at all from the official Spotify app, or speed things up a lot. 

For example:
Maybe someone like me wants to make a public playlist from a "favorite" playlist,
but alas it is impossible in the application,
so I created a function "copy_favorite_tracks_to_public_playlist".

Currently, there are the following features:

- creating a public playlist from a favourite


- creation of N public playlists, each with 100 tracks,
for convenient downloading via third-party services (e.g. https://spotify-downloader.com/),
this is not an advertisement.


- The function that remove the prefix of the service https://spotify-downloader.com/,
which it adds to each track and accordingly the search by name disappears.


- The function that export titles of tracks from public playlist to .txt file 
with sorting by alphabet or not (as you want)


- The function that will allow you to transfer all your tracks from "Favorites"
from account #1 to account #2 in the same order. (speed 1 track per second)


- The function that will allow you to overwrite your Favorites playlist
with tracks from a public playlist. 
(This is necessary if you, for example, have always used a public playlist to store
tracks there, and now you can overwrite it with your favorites).


- The function that delete all tracks from favorites 


- The function that delete the cache

After cloning the project, install the required libraries using pip :
<br> 
**pip install -r requirements.txt**