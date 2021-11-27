# import boto3
# from .db import DBInstance
# import traceback

# class DynamoModel:
#     def __init__(self, modelName):
#         try:
#             model = DBInstance.Table(modelName)
#             self.model = model
#             self.model_name = modelName
#         except:
#             print("some error while getting model")
#             traceback.print_exc()
    
#     def write_items(self,data):
#         try:
#             with self.model.batch_writer(overwrite_by_pkeys=['partition_key']) as writer:
#                 for obj in data:
#                     writer.put_item(Item=obj)
#         except:
#             print("some error while getting model")
#             traceback.print_exc()
    
#     def write_item(self, data):
#         try:
#             self.model.put_item(Item=data)
#         except:
#             print("some error while getting model")
#             traceback.print_exc()
    
#     def get_item(self, key):
#         try:
#             response = self.model.get_item(Key= { 'id' : key })
#             return response.get("Item") 
#         except:
#             print("some error while getting model")
#             traceback.print_exc()
    
#     def list_items(self,scan_filter=None, LastEvaluatedKey = None, limit = 25):
#         try:
#             scan_params = {}
#             if LastEvaluatedKey:
#                 scan_params['ExclusiveStartKey'] =  LastEvaluatedKey
#             if scan_filter:
#                 scan_params['ExpressionAttributeValues'] = {
#                     ':v1': str('https://p.scdn.co/mp3-preview/f3f285165dd5d24fe7174e6dcebd60dcc05a2d73?cid=f3e2aa70da71420db6b89390dd73a075')
#                 }
#                 scan_params['FilterExpression'] = "preview_url = :v1"
#             response = self.model.scan(**scan_params)    
#             data = response.get('Items')
#             if not data:
#                 data = []
#             while 'LastEvaluatedKey' in response and len(data) < limit:
#                 scan_params['ExclusiveStartKey']  = response['LastEvaluatedKey']
#                 response = self.model.scan(**scan_params)
#                 data.extend(response['Items'])
#             return data[:limit]
#         except:
#             print("some error while getting items")
#             traceback.print_exc()
#             raise
    
#     def get_items_by_key(self, keys):
#         try:
#             response = {}
#             for key in keys:
#                 results = self.model.query(
#                     ExpressionAttributeValues={
#                         ":v1": str(key)
#                     },
#                     KeyConditionExpression='id = :v1'
#                 )
#                 response[key] = results['Items'][0]
#             # RequestItems = {
#             #     self.model_name: {
#             #         "Keys": [
#             #             {
#             #                 "id": { "S" : "0OFfw3MUbUIzvIFeRDjR2N" }
#             #             }]
#             #         }
#             #     }
#             # print(RequestItems)
#             # response = DBInstance.batch_get_item(
#             #     RequestItems=RequestItems
#             # )
#             return response
#         except:
#             print("some error while getting items by key")
#             traceback.print_exc()
#             raise
    
    