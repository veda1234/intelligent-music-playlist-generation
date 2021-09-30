import requests
import json
import os
from authenticator import Authenticator

SPOTIFY__CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') 
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')

authObj = Authenticator()

def process_data(data):
    print(data)

def get_audio_features(track_ids, auth_token):
    endpoint = "https://api.spotify.com/v1/audio-features"
    headers = {"Authorization": "Bearer {0}".format(auth_token) }
    response = requests.get(endpoint,headers=headers, params={ "ids": {track_ids}})
    if response.status_code == 401:
        auth_token = authObj.get_auth_token()
        get_audio_features(track_ids,auth_token)
    elif response.status_code == 200:
        return process_data(json.dumps(response.json(),indent=4))
    else:
        return response.status_code

if __name__ == '__main__':
    token = authObj.get_auth_token()
    track_ids = "4JpKVNYnVcJ8tuMKjAj50A,2NRANZE9UCmPAS5XVbXL40,24JygzOLM0EmRQeGtFcIcG"
    if token and track_ids:
        get_audio_features(track_ids, token)
    elif not token:
        print('Invalid token')
    else:
        print('Invalid track ids')