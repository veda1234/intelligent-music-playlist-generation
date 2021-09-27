import os
import requests
from authenticator import Authenticator

# included columns => id, preview_url, album.artists[name,id],album.id
# album.release_date,album.release_date_precision,album.album_type,popularity, preview_url

SPOTIFY__CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') 
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
URL = "https://api.spotify.com/v1/tracks"



def get_metadata(track_ids, auth_token):
    headers = {"Authorization": "Bearer {0}".format(auth_token) }
    response = requests.get(URL,headers=headers, params={ "ids": ",".join(track_ids) })
    return response.json()

if __name__ == '__main__':
    authObj = Authenticator()
    token = authObj.get_auth_token()
    track_ids = input().split(',')
    if token and track_ids:
        print(get_metadata(track_ids, token))
    elif not token:
        print('Invalid token')
    else:
        print('Invalid track ids')