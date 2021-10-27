import boto3
import logging
from decimal import Decimal
import os
import json
logger = logging.getLogger(__name__)

AUDIO_FEATURES = 'dataset/'

def write_to_dynamodb(filename, writer):
    object_array = json.load(open(filename, 'r'),parse_float=Decimal)
    for obj in object_array:
        writer.put_item(Item=obj)


def write_data(filepath, table):        
    files = os.listdir(filepath)
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

    audio_features_table = dynamodb.Table('audio_features')
    write_data(AUDIO_FEATURES, audio_features_table)
# aws_access_key_id = AKIA3I5JUJH4B55QIT7N
# aws_secret_access_key = 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