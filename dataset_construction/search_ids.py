# Get ids from here
# Need to extract ids from this json
import requests
import json
import os

from authenticator import Authenticator

SPOTIFY__CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') 
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')

authObj = Authenticator()

def process_data(data):
    print(data)

def get_search_tracks(auth_token):
    endpoint = "https://api.spotify.com/v1/search"
    headers = {"Authorization": "Bearer {0}".format(auth_token) }
    # Fill any keyword from a playlist and place value in q, it will match substring as well
    # Reputation is a taylor swift album. You can try any other words, like fearless, time, lover etc. It will give all 
    # tracks matching the
    response = requests.get(endpoint,headers=headers, params={"q": "Reputation", "type": "track"})
    if response.status_code == 401:
        auth_token = authObj.get_auth_token()
        get_search_tracks(track_ids,auth_token)
    elif response.status_code == 200:
        return process_data(json.dumps(response.json(),indent=4))
    else:
        return response.status_code

if __name__ == '__main__':
    token = authObj.get_auth_token()
    track_ids = "4JpKVNYnVcJ8tuMKjAj50A,2NRANZE9UCmPAS5XVbXL40,24JygzOLM0EmRQeGtFcIcG"
    if token and track_ids:
        get_search_tracks(token)
    elif not token:
        print('Invalid token')
    else:
        print('Invalid track ids')