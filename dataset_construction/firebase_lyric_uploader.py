import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle
import json
import os
import traceback
import sys
import boto3

dynamodb = boto3.resource('dynamodb',
                        aws_access_key_id='AKIA3LSMMJ36YIMMQKOI', 
                        aws_secret_access_key='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', 
                        region_name='us-east-2')

audio_features = dynamodb.Table('audio_features')

# Use a service account
cred = credentials.Certificate('../credentials/firestore-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

LYRIC_DATA_PATH = '../dataset/lyrics'


def upload_lyric_file(filename, st_index = 0):
    lyrics = json.load(open(filename, 'r'))
    for i,lyric in enumerate(list(lyrics.keys())[st_index:]):
        try:
            af = audio_features.get_item(Key= { 'id' : lyric }).get("Item")
            if af == None:
                continue
            for key in af:
                if key == 'id':
                    af[key] = str(af[key])
                elif key in ['duration_ms', 'mode', 'time_signature', 'key']:
                    af[key] = int(af[key])
                else:
                    af[key] = float(af[key])
            db.collection('track_features').document(lyric).set({
                "lyrics": lyrics[lyric],
                "audio_features": af,
            })
        except:
            print(f'error at uploading lyric for index: {st_index + i}')
            raise

if __name__ == '__main__':
    lyric_files = sorted(os.listdir(LYRIC_DATA_PATH))
    i = 0
    print(len(lyric_files))
    for file in lyric_files[131:]:
        try:
            if i == 0:
                upload_lyric_file(LYRIC_DATA_PATH + '/' + file,126)
            else:
                upload_lyric_file(LYRIC_DATA_PATH + '/' + file)
            i += 1
            if i % 10 == 0:
                print('{0} done'.format(i))
        except:
            print(f'some error at lyric file index: {i}')
            traceback.print_exc()
            sys.exit(1)
        