# Get ids from here
# Need to extract ids from this json
import requests
from urllib.parse import urlencode
import json
from authenticate import SpotifyAPI
import pandas as pd
from io import StringIO
from config import client_id, client_secret

spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
access_token = spotify.access_token
headers = {
    "Authorization": f"Bearer {access_token}"
}

endpoint = "https://api.spotify.com/v1/search"
# Fill any keyword from a playlist and place value in q, it will match substring as well
# Reputation is a taylor swift album. You can try any other words, like fearless, time, lover etc. It will give all 
# tracks matching the
data = urlencode({"q": "Reputation", "type": "track"}) 

lookup_url = f"{endpoint}?{data}"
r = requests.get(lookup_url, headers=headers)
data_json = json.dumps(r.json(), indent=4)
print(data_json)

# data_obj = r.json()

# for track in data_obj['tracks']:
#     print(track["next"])