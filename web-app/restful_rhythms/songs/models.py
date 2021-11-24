from common_utils import DynamoModel
import traceback


class TrackClass(DynamoModel):
    def __init__(self):
        super(TrackClass, self).__init__('tracks')
    
    def get_songs(self, prevRecord = None, limit = 25):
        try:
            LastEvaluatedKey = None
            if prevRecord:
                LastEvaluatedKey["id"] = prevRecord["id"]
                LastEvaluatedKey["name"] = prevRecord["name"]
            songs = super().get_items(limit = 25, LastEvaluatedKey=prevRecord)
            return songs
        except:
            print("some error occured in fetching songs")
            traceback.print_exc()
            raise

Track = TrackClass()