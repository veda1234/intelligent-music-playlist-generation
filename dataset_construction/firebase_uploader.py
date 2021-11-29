import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle
import json
import os

# Use a service account
cred = credentials.Certificate('../credentials/firestore-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()



track_clusters = pickle.load(open('../dataset/final_results.pkl', 'rb'))
track_lyrics = pickle.load(open('../dataset/track_lyric_emotions.pkl','rb'))

TRACK_DATA_PATH = '../dataset/clean_tracks'
ALBUM_DATA_PATH = '../dataset/clean_albums'

def upload_track_file(file):
    tracks = json.load(open(file, 'r'))
    album_ids = set()
    for track in tracks:
        if (track['id'] in track_lyrics) and (track['id'] in track_clusters):
            track['cluster'] = track_clusters[track['id']]
            track['emotion'] = track_lyrics[track['id']]
            album_ids.add(track['album_id'])
            db.collection('tracks').document(track['id']).set(track)
    return album_ids

def upload_album_file(file, album_ids):
    albums = json.load(open(file, 'r'))
    for album in albums:
        if album['id'] in album_ids:
            db.collection('albums').document(album['id']).set(album)


if __name__ == '__main__':
    track_files = os.listdir(TRACK_DATA_PATH)
    i = 0
    album_ids = set()
    for file in track_files:
        curr_album_ids = upload_track_file(TRACK_DATA_PATH + '/' + file)
        album_ids = album_ids.union(curr_album_ids)
        i += 1
        if i % 10 == 0:
            print('{0} done'.format(i))
        
    album_files = os.listdir(ALBUM_DATA_PATH)
    i = 0
    for file in album_files:
        upload_album_file(ALBUM_DATA_PATH + '/' + file, album_ids)
        i += 1
        if i % 10 == 0:
            print('{0} done'.format(i))
    
    