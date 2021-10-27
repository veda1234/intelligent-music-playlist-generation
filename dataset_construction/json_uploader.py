import boto3
import logging
import os
import json
logger = logging.getLogger(__name__)

ALBUM_DATA_PATH = '../dataset/clean_albums'
TRACK_DATA_PATH = '../dataset/clean_tracks'


def write_to_dynamodb(filename, writer):
    object_array = json.load(open(filename, 'r'))
    for obj in object_array:
        if (not obj["name"]) or obj["name"] == "":
            obj["name"] = "--"
        writer.put_item(Item=obj)


def write_data(filepath, table):        
    files = os.listdir(filepath)
    clean_json = []
    i = 0
    with table.batch_writer() as writer:
        for file in files:
            write_to_dynamodb(filepath + '/' + file,writer)
            i += 1
            if i % 10 == 0:
                print('{0} done'.format(i))

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb',
                            aws_access_key_id='AKIA3LSMMJ36YIMMQKOI', 
                            aws_secret_access_key='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', 
                            region_name='us-east-2')

    album_table = dynamodb.Table('albums')
    track_table = dynamodb.Table('tracks')
    write_data(ALBUM_DATA_PATH, album_table)
    write_data(TRACK_DATA_PATH, track_table)
    



