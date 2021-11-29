# import boto3
# import json
# import traceback

# CREDENTIALS_FILE = '../../credentials/web_app_credentials.json'

# DBInstance = None
# try:
#     credentials = json.load(open(CREDENTIALS_FILE, 'r'))
#     dynamodb_credentials = credentials['dynamo_db'] 
#     dynamoDB = boto3.resource('dynamodb',
#                             aws_access_key_id=dynamodb_credentials['access_key_id'], 
#                             aws_secret_access_key=dynamodb_credentials['access_key_secret'], 
#                             region_name=dynamodb_credentials['region'])
#     DBInstance = dynamoDB
# except:
#     print("some error while connecting to dynamo db")
#     traceback.print_exc()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle
import json
import traceback

DBInstance = None
try:
# Use a service account
    cred = credentials.Certificate('../../credentials/firestore-key.json')
    firebase_admin.initialize_app(cred)

    DBInstance = firestore.client()
except:
    print('error in initializing firestore db')
    traceback.print_exc()
    raise