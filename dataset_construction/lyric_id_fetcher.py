import requests
import pickle
import traceback
import os
import json

TRACK_DATA_PATH = '../dataset/clean_tracks'
TRACK_URL_PATH = '../dataset/track_lyric_urls.pkl'


def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'juoL7CJICtYLC5L2z-SpZPXL4sykzlPkvaxsFUlRFqM5dTaJe6rM7kB4p3A08zHH'}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, params=data, headers=headers)
    return response


def get_data_for_tracks_file(file, st_index=0):
    global track_urls
    filename = TRACK_DATA_PATH + '/' + file
    object_array = json.load(open(filename, 'r'))
    for i,obj in enumerate(object_array[st_index:]):
        song_name = obj['name']
        artist_name = obj['artists'][0]['name'].lower()
        try:
            resp = request_song_info(song_name, artist_name)
            resp_json = resp.json()
            remote_song_info = None
            for hit in resp_json['response']['hits']:
                condition = True
                for word in artist_name.split(' '):
                    condition = condition and (word  in  hit['result']['primary_artist']['name'].lower())
                if condition:
                    remote_song_info = hit['result']['url']
                    break
            track_urls[obj["id"]] = remote_song_info
        except:
            print("error at track index: {0} for song name {1} by {2}".format(st_index + i, song_name, artist_name))
            traceback.print_exc()
            raise

    
if __name__ == '__main__':
    global track_urls   
    track_urls = {}     
    files = sorted(os.listdir(TRACK_DATA_PATH))
    i = 0
    if os.path.exists(TRACK_URL_PATH):
        track_urls = pickle.load(open(TRACK_URL_PATH, 'rb'))
    print(len(files))
    for file in files[75:]:
        try:
            if i == 0:
                get_data_for_tracks_file(file, 811)
            else:
                get_data_for_tracks_file(file)
            print('{0} th file done'.format(i))
            i += 1
        except:
            print("error at track file index: {0}".format(i))
            traceback.print_exc()
            pickle.dump(track_urls, open(TRACK_URL_PATH, 'wb'))
            raise
    pickle.dump(track_urls, open(TRACK_URL_PATH, 'wb'))