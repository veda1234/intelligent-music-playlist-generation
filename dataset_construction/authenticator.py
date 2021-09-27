import os
import requests
from requests.api import head 
from requests.auth import HTTPBasicAuth
import time
import sys
import traceback

SPOTIFY__CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') 
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')

URL = "https://accounts.spotify.com/api/token"
GRANT_TYPE = "client_credentials"


class Authenticator:

    def __init__(self):
        self.token = None
        self.expiry = None
    
    def get_auth_token(self):
        if (not self.expiry) or time.time() > self.expiry:
         self.token,self.expiry = self._get_auth_token()
        return self.token

    def _get_auth_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(URL,data={ "grant_type": GRANT_TYPE }, 
                auth=HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY__CLIENT_SECRET),
                headers=headers,
                )
            print(response.json())
            response_dict = response.json()
            return (response_dict["access_token"], time.time() + response_dict['expires_in'])
        except:
            print(sys.exc_info()[2])
            print(traceback.format_exc())
            return None




