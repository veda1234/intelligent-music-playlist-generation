import requests
import json
from os.path import exists
import pickle
import os

from requests.api import get
from authenticator import Authenticator

SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET') 
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')

authObj = Authenticator()

count = 0

def process_data(data,number):
    json_data = data.json()
    audio_f = json_data["audio_features"]
    final_features = []
    for features in audio_f:
        if not features:
            global count
            count+=1
            print(features)
            continue
        else:
            collect_features = {  "danceability" : features["danceability"], 
                        "energy": features["energy"],
                        "key": features["key"],
                        "loudness": features["loudness"],
                        "mode" : features["mode"], 
                        "speechiness": features["speechiness"],
                        "acousticness": features["acousticness"],
                        "instrumentalness": features["instrumentalness"],
                        "liveness": features["liveness"],
                        "valence": features["valence"],
                        "tempo" : features["tempo"], 
                        "id": features["id"],
                        "duration_ms": features["duration_ms"],
                        "time_signature": features["time_signature"] }
            final_features.append(collect_features)
            print(features["danceability"])
    path_to_file = 'dataset/audio_features'+str(number)+'.json'
    if exists(path_to_file):
        if final_features:
            with open(path_to_file,'r') as fp:
                prev_data = json.load(fp)
                prev_data.extend(final_features)
            with open(path_to_file,'w') as fp:
                json.dump(prev_data,indent=4,fp=fp)
    else:
        if final_features:
            with open(path_to_file,'w') as fp:
                json.dump(final_features,indent=4,fp=fp)

def get_audio_features(track_ids, auth_token):
    total_length = len(track_ids)
    for j in range(0,total_length,5000):
        for i in range(j,min(j+5000,total_length),100):
            endpoint = "https://api.spotify.com/v1/audio-features"
            headers = {"Authorization": "Bearer {0}".format(auth_token) }
            response = requests.get(endpoint,headers=headers, params={ "ids": ",".join(track_ids[i:min(i+100,total_length)]) })
            print(response.status_code)
            if response.status_code == 401:
                auth_token = authObj.get_auth_token()
                headers = {"Authorization": "Bearer {0}".format(auth_token) }
                response = requests.get(endpoint,headers=headers, params={ "ids": ",".join(track_ids[i:min(i+100,total_length)]) })
                process_data(response,min(j+5000,total_length))
            elif response.status_code == 200:
                process_data(response,min(j+5000,total_length))
            else:
                return response.status_code

def process_info(_):
    pass

if __name__ == '__main__':
    with open('store_ids.pickle', 'rb') as f:
        track_ids = pickle.load(f)
    track_ids = list(track_ids)
    token = authObj.get_auth_token()
    if token and track_ids:
        get_audio_features(track_ids, token)
    elif not token:
        print('Invalid token')
    else:
        print('Invalid track ids')
    print(count)