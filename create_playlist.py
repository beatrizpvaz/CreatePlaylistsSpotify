import json
import os
import requests
import datetime

from secrets import spotify_token, spotify_user_id
from exceptions import ResponseException


class CreatePlaylist:
    def __init__(self):
        self.songs_info = {}

    def create_playlist(self, date):
        """Creates a new playlist"""
        request_body = json.dumps({
            "name": "Songs from {}".format(date),
            "description": "Creating Playlists based on Liked songs and organised per day",
            "public": False
        })

        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        return response_json["id"]

    def get_my_songs(self):
        """Gets songs in my Library"""

        query = "https://api.spotify.com/v1/me/tracks"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()

        for item in response_json['items']:
            artist = item['track']['album']['artists'][0]['name']
            song = item['track']['name']
            date_added = datetime.datetime.strptime(item['added_at'][:10], '%Y-%m-%d').date()
            uri = item['track']['uri']

            if date_added not in self.songs_info:
                self.songs_info[date_added] = [uri]
            elif uri not in self.songs_info[date_added]:
                self.songs_info[date_added].append(uri)

    def check_existing_playlists(self):
        """Checking the existing playlists"""

        query = 'https://api.spotify.com/v1/me/playlists'
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        response_json = response.json()
        playlists = {}
        for item in response_json['items']:
            playlists[item['name']] = item['id']
        return playlists

    def add_songs_to_existing_playlists(self, key, value, playlists):
        """If a playlist for a certain date already exists, take a look
        at the songs there and if there are any news songs to be added to this day,
        add them
        """

        playlist_name = 'Songs from {}'.format(key)
        playlist_id = playlists[playlist_name]

        query = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        playlist_items = set()
        for item in response_json['items']:
            playlist_items.add(item['track']['uri'])

        # This avoids the next for loop by checking whether there is any new songs
        # in Liked folder to add to the existing playlist
        value_set = set(value)
        if value_set == playlist_items:
            return

        for song in value_set:
            if song not in playlist_items:
                request_data = json.dumps([song])
                query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

                response = requests.post(
                    query,
                    data=request_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(spotify_token)}
                )

    def add_songs_to_playlists(self):
        """Adds songs to the created playlists"""

        self.get_my_songs()
        playlists = self.check_existing_playlists()

        for key, value in self.songs_info.items():
            if 'Songs from {}'.format(key) in playlists.keys():
                self.add_songs_to_existing_playlists(key, value, playlists)

            else:
                playlist_id = self.create_playlist(key)
                request_data = json.dumps(value)

                query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

                response = requests.post(
                    query,
                    data=request_data,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(spotify_token)}
                )

                if response.status_code != 200 or response.status_code != 201:
                    raise ResponseException(response.status_code)


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_songs_to_playlists()