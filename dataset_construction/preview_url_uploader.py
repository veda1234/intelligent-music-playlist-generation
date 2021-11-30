import boto3
import logging
import os
import json
logger = logging.getLogger(__name__)
import requests

TRACK_DATA_PATH = '../dataset/clean_tracks'
TEST_AUDIO_PATH = '../dataset/audio_1.mp3'


s3_client = boto3.client('s3')

def write_to_S3(filename):
    global count
    object_array = json.load(open(filename, 'r'))
    for obj in object_array:
        if obj['preview_url']:
            resp = requests.get(obj['preview_url'])
            open(TEST_AUDIO_PATH, 'wb').write(resp.content)
            s3_client.upload_file(TEST_AUDIO_PATH, 'emoti-tune', '{0}.mp3'.format(obj['id']))
            count += 1
            if count == 1500:
                break

if __name__ == '__main__':
    global count
    count = 0
    files = sorted(os.listdir(TRACK_DATA_PATH))
    try:
        for file in files:
            write_to_S3(TRACK_DATA_PATH + '/' + file)
            if count == 1500:
                break
            if count % 10 == 0:
                print(f'{count} done')
    except:
        print(f'error at {count}')
        raise

