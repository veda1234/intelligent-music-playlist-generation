from common_utils import FirestoreModel
import traceback


class TrackClass(FirestoreModel):
    def __init__(self):
        super(TrackClass, self).__init__('tracks')
    
    def get_songs(self,query_params={}, prevRecord = None, limit = 25):
        try:
            LastEvaluatedKey = None
            query = []
            for key in query_params:
                if key in ['cluster','id','emotion']:
                    query.append((key,'in',query_params[key]))
                else:
                    query.append((key, '==', query_params[key]))
            songs = super().list_items(query=query, limit = 25, LastEvaluatedKey=prevRecord)
            return songs
        except:
            print("some error occured in fetching songs")
            traceback.print_exc()
            raise


class UserTrackClass(FirestoreModel):
    def __init__(self):
        super(UserTrackClass, self).__init__('track_users',keyField='user_id')
    
    def get_user_songs(self, user_id):
        try:
            user_songs = super().get_item(user_id)
            if user_songs == None:
                return user_songs
            else:
                return user_songs['songs']
        except:
            print(f"some error occured in fetching songs for user {user_id}")
            traceback.print_exc()
            raise

Track = TrackClass()
UserTrack = UserTrackClass()