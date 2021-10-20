import os
import requests
from authenticator import Authenticator
import pickle
import json

TRACK_ID_PATH = '../dataset/track_ids.pkl'
TRACK_DATA_PATH = '../dataset/tracks'
TRACK_API_URL = 'https://api.spotify.com/v1/tracks'

class TrackDataManager:
    def __init__(self):
        self.new_track_ids = set()
        self.track_data = []
        if os.path.exists(TRACK_ID_PATH):
            track_id_file = open(TRACK_ID_PATH,'rb')
            self.track_ids = pickle.load(track_id_file)
            track_id_file.close()
        else:
            self.track_ids = set()
        self.authenticator = Authenticator()
    
    def get_track_data(self, response_dict):
        result_list  = []
        for track in response_dict["tracks"]:
            if not track:
                continue
            artists = [{ "name" : artist["name"], "id" : artist["id"] } for artist in track["artists"]]
            curr_track = { "id" : track["id"], 
                           "name": track["name"],
                           "popularity": track["popularity"],
                           "preview_url": track["preview_url"],
                           "artists": artists,
                           "duration": track["duration_ms"],
                           "album_id": track["album"]["id"],
                    }
            result_list.append(curr_track)
        return result_list
    
    def write_track_data(self):
        files = os.listdir(TRACK_DATA_PATH)
        new_num = len(files) + 1
        out_f = open(TRACK_DATA_PATH + '/track_data_{0}.json'.format(new_num), 'w')
        out_f.write(json.dumps(self.track_data, indent=4))
        out_f.close()
    
    def write_track_ids(self):
        o_file = open(TRACK_ID_PATH, 'wb')
        pickle.dump(self.track_ids, o_file)
        o_file.close()


    def fetch_track_data(self, track_ids=None, write_anyways=False):
        if not track_ids:
            track_ids = self.new_track_ids
        if len(self.new_track_ids) == 0:
            return
        token = self.authenticator.get_auth_token()
        headers = {"Authorization": "Bearer {0}".format(token) }
        response = requests.get(TRACK_API_URL,headers=headers, params={ "ids": ",".join(track_ids) })
        if response.status_code == 200:
            self.track_data.extend(self.get_track_data(response.json()))
            self.track_ids = self.track_ids.union(self.new_track_ids)
            self.new_track_ids = set()
            if len(self.track_data) >= 5000 or write_anyways:
                self.write_track_data()
                self.track_data = []
                self.write_track_ids()    
        else:
            print('some error in fetching the ids')
            print('status code: ', response.status_code)
            print('error: ', response.text)


    def add_track(self,track_id):
        if track_id not in self.track_ids:
            self.new_track_ids.add(track_id)
            if len(self.new_track_ids) >= 20:
                self.fetch_track_data(self.new_track_ids)
    

if __name__ == '__main__':
    trackM = TrackDataManager()
    trackM.add_track('612VcBshQcy4mpB2utGc3H')
    trackM.add_track('3LcYYV9ozePfgYYmXv0P3r')
    trackM.add_track('54eZmuggBFJbV7k248bTTt')
    trackM.add_track('40riOy7x9W7GXjyGp4pjAv')
    