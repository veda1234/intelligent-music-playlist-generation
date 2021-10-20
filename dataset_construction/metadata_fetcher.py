import os
import requests
from authenticator import Authenticator

# included columns => id, preview_url, album.artists[name,id],album.id
# album.release_date,album.release_date_precision,album.album_type,popularity, preview_url

SPOTIFY__CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') 
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
URL = "https://api.spotify.com/v1/tracks"
authObj = Authenticator()

def process_data(data):
    albums = {}
    tracks = {}
    for track in data['tracks']:
        curr_row = {  "id" : track["id"], 
                      "preview_url": track["preview_url"],
                      "album_id": track["album"]["id"],
                      "popularity": track["popularity"] }
        tracks[track["id"]] = curr_row
        album = track["album"]
        artists = [{ "name" : artist["name"], "id" : artist["id"] } for artist in album["artists"]]
        if album["id"] not in albums:
            curr_album = { "id" : album["id"], 
                       "release_date": album["release_date"],
                       "release_date_precision": album["release_date_precision"],
                       "album_type": album["album_type"],
                       "artists": artists,
                    }
            albums[album["id"]] = curr_album
    return albums, tracks
    
def get_metadata(track_ids, auth_token):
    headers = {"Authorization": "Bearer {0}".format(auth_token) }
    response = requests.get(URL,headers=headers, params={ "ids": ",".join(track_ids) })
    if response.status_code == 401:
        auth_token = authObj.get_auth_token()
        get_metadata(track_ids,auth_token)
    elif response.status_code == 200:
        return process_data(response.json())
    else:
        return response.status_code



if __name__ == '__main__':
    token = authObj.get_auth_token()
    track_ids = input().split(',')
    if token and track_ids:
        albums,tracks = get_metadata(track_ids, token)
        print(albums, tracks)
    elif not token:
        print('Invalid token')
    else:
        print('Invalid track ids')