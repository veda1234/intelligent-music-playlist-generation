import boto3
import json
import traceback

CREDENTIALS_FILE = '../../credentials/web_app_credentials.json'

DBInstance = None
try:
    credentials = json.load(open(CREDENTIALS_FILE, 'r'))
    dynamodb_credentials = credentials['dynamo_db'] 
    dynamoDB = boto3.resource('dynamodb',
                            aws_access_key_id=dynamodb_credentials['access_key_id'], 
                            aws_secret_access_key=dynamodb_credentials['access_key_secret'], 
                            region_name=dynamodb_credentials['region'])
    DBInstance = dynamoDB
except:
    print("some error while connecting to dynamo db")
    traceback.print_exc()