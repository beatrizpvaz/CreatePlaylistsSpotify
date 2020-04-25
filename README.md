## CREATING SPOTIFY PLAYLISTS

A simple script that takes the items in your Spotify library and creates playlists in order to group them by date added to the Liked songs.

This project is inspired in this one https://github.com/TheComeUpCode/SpotifyGeneratePlaylist

# Getting Spotify id and Oauth token
To get you id, log into Spotify and go to https://www.spotify.com/us/account/overview/ . Your username is your id

To get the token you need to register to Spotify Developer, go to https://developer.spotify.com/console/post-playlists/ , click on Get Token and check all the boxes.

Copy both the id and Oauth token to a secrets file.

# Warning
The Oauth token expires quite quickly. If you get a KeyError due to this, create another token.