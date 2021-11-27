import boto3
from .db import DBInstance
import traceback

class FirestoreModel:
    def __init__(self, modelName, keyField='id',is_collection_group=False):
        try:
            if is_collection_group:
                model = DBInstance.collection_group(modelName)
            else:
                model = DBInstance.collection(modelName)
            self.model = model
            self.model_name = modelName
            self.key_field = keyField
        except:
            print("some error while getting model")
            traceback.print_exc()
    
    def write_items(self,data):
        try:
            batch = DBInstance.batch()
            for obj in data:
                batch.set(self.model.document(obj[self.key_field]), obj)
            batch.commit()   
        except:
            print("some error while writing multiple items")
            traceback.print_exc()
    
    def write_item(self, data):
        try:
            self.model.document(data[self.key_field]).set(data)
        except:
            print("some error while writing item")
            traceback.print_exc()
    
    def get_item(self, key):
        try:
            response = self.model.document(key).get()
            return response.to_dict()
        except:
            print("some error while getting item")
            traceback.print_exc()
    
    def list_items(self,query=None, LastEvaluatedKey = None, limit = 25):
        try:
            cursor = self.model
            if query:
                for q in query:
                    cursor = self.model.where(*q)
            if LastEvaluatedKey:
                last_doc = self.model.document(LastEvaluatedKey).get()
                cursor = cursor.order_by(self.key_field).start_after({ self.key_field: LastEvaluatedKey })
            cursor = cursor.limit(limit)
            return [record.to_dict() for record in cursor.stream()]
        except:
            print("some error while getting items")
            traceback.print_exc()
            raise
    
    def get_items_by_key(self, keys):
        try:
            key_query = (self.key_field, 'in', [keys])
            records = self.list_items(query=[key_query],limit=100)
            return { record['id'] : record for record in records }
        except:
            print("some error while getting items by key")
            traceback.print_exc()
            raise
    
    