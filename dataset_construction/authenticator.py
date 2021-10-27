import os
import requests
from requests.api import head 
from requests.auth import HTTPBasicAuth
from datetime import timedelta, datetime
import sys
import traceback

SPOTIFY__CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') 
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')

URL = "https://accounts.spotify.com/api/token"
GRANT_TYPE = "client_credentials"
TOKEN_PATH = "../credentials/client_credentials_token"


class Authenticator:

    def __init__(self):
        if os.path.exists(TOKEN_PATH):
            token_file = open(TOKEN_PATH,'r')
            self.token, self.expiry = token_file.read().split('\n')
            self.expiry = datetime.fromisoformat(self.expiry)
            token_file.close()
        else:
            self.token = None
            self.expiry = None
    
    def get_auth_token(self):
        if (not self.expiry) or datetime.now() > self.expiry:
         self.token,self.expiry = self._get_auth_token()
         token_file = open(TOKEN_PATH, 'w')
         token_file.write(self.token + '\n' + str(self.expiry))
        return self.token

    def _get_auth_token(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(URL,data={ "grant_type": GRANT_TYPE }, 
                auth=HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY__CLIENT_SECRET),
                headers=headers,
                )
            response_dict = response.json()
            return (response_dict["access_token"], datetime.now() + timedelta(0,response_dict['expires_in']))
        except:
            print(sys.exc_info()[2])
            print(traceback.format_exc())
            return None
