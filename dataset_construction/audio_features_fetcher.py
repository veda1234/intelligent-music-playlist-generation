import requests
import datetime
from urllib.parse import urlencode
import base64
import json
from authenticate import SpotifyAPI
from config import client_id, client_secret

spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
access_token = spotify.access_token
headers = {
    "Authorization": f"Bearer {access_token}"
}


endpoint = "https://api.spotify.com/v1/audio-features"
data = urlencode({"ids":"4JpKVNYnVcJ8tuMKjAj50A,2NRANZE9UCmPAS5XVbXL40,24JygzOLM0EmRQeGtFcIcG"})

lookup_url = f"{endpoint}?{data}"
print(lookup_url)
r = requests.get(lookup_url, headers=headers)
print(json.dumps(r.json(),indent=4))