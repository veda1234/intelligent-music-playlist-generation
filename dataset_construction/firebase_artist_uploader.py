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

if __name__ == '__main__':
    artist_ref = db.collection('artists')
    track_ref = db.collection('tracks')
    i = 0
    r = None
    try:
        for record in db.collection('tracks').order_by('id').start_at({ 'id': '10AROvgxHe4dzZ8Cxh6Yay' }).stream():            
            r  = record.to_dict()
            for artist in r['artists']:
                artist_ref.document(artist['id']).set(artist)
            i += 1
            track_ref.document(r['id']).update({ 'artist_id': [artist['id'] for artist in r['artists']] })
            if i % 100 == 99:
                print(f'{i+1} done')
    except:
        print(f'error at {r}')
        raise

    