import os
import requests
from authenticator import Authenticator
import pickle
import json

album_ids = set()
ALBUM_ID_PATH = '../dataset/album_ids.pkl'
ALBUM_DATA_PATH = '../dataset/albums'
ALBUM_API_URL = 'https://api.spotify.com/v1/albums'

class AlbumDataManager:
    def __init__(self):
        self.new_album_ids = set()
        self.album_data = []
        if os.path.exists(ALBUM_ID_PATH):
            album_id_file = open(ALBUM_ID_PATH,'rb')
            self.album_ids = pickle.load(album_id_file)
            album_id_file.close()
        else:
            self.album_ids = set()
        self.authenticator = Authenticator()
    
    def get_album_data(self, response_dict):
        result_list  = []
        for album in response_dict["albums"]:
            if not album:
                continue
            artists = [{ "name" : artist["name"], "id" : artist["id"] } for artist in album["artists"]]
            curr_album = { "id" : album["id"], 
                       "release_date": album["release_date"],
                       "release_date_precision": album["release_date_precision"],
                       "album_type": album["album_type"],
                       "artists": artists,
                       "name": album["name"]
                    }
            result_list.append(curr_album)
        return result_list
    
    def write_album_data(self):
        files = os.listdir(ALBUM_DATA_PATH)
        new_num = len(files) + 1
        out_f = open(ALBUM_DATA_PATH + '/album_data_{0}.json'.format(new_num), 'w')
        out_f.write(json.dumps(self.album_data, indent=4))
        out_f.close()
    
    def write_album_ids(self):
        o_file = open(ALBUM_ID_PATH, 'wb')
        pickle.dump(self.album_ids, o_file)
        o_file.close()


    def fetch_album_data(self, album_ids=None, write_anyways=False):
        if not album_ids:
            album_ids = self.new_album_ids
        if len(self.new_album_ids) == 0:
            return
        token = self.authenticator.get_auth_token()
        headers = {"Authorization": "Bearer {0}".format(token) }
        response = requests.get(ALBUM_API_URL,headers=headers, params={ "ids": ",".join(album_ids) })
        if response.status_code == 200:
            self.album_data.extend(self.get_album_data(response.json()))
            self.album_ids = self.album_ids.union(self.new_album_ids)
            self.new_album_ids = set()
            if len(self.album_data) >= 5000 or write_anyways:
                self.write_album_data()
                self.album_data = []
                self.write_album_ids()    
        else:
            print('some error in fetching the ids')
            print('status code: ', response.status_code)
            print('error: ', response.text)


    def add_album(self,album_id):
        if album_id not in self.album_ids:
            self.new_album_ids.add(album_id)
            if len(self.new_album_ids) >= 20:
                self.fetch_album_data(self.new_album_ids)
    

if __name__ == '__main__':
    albumM = AlbumDataManager()
    albumM.add_album('6vV5UrXcfyQD1wu4Qo2I9K')
    albumM.add_album('0z7pVBGOD7HCIB7S8eLkLI')
    albumM.add_album('25hVFAxTlDvXbx2X2QkUkf')
    albumM.add_album('6QPkyl04rXwTGlGlcYaRok')
    