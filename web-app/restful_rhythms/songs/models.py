from common_utils import FirestoreModel
import traceback


def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

class TrackClass(FirestoreModel):
    def __init__(self):
        super(TrackClass, self).__init__('tracks')
    
    def get_songs(self,query_params={}, prevRecord = None, nextRecord=None, limit = 25):
        try:
            query = []
            split_ids = None
            if query_params.get('id'):
                split_ids = chunks(query_params['id'], 10)   
            for key in query_params:
                if key == 'artist_id':
                    query.append((key, 'array_contains', query_params[key]))
                elif (key != 'id'):
                    query.append((key, '==', query_params[key]))
            if not split_ids:
                songs = super().list_items(query=query, limit = 25, LastEvaluatedKey=prevRecord, nextRecord = nextRecord)
                return songs
            songs = []
            for split_id in split_ids:
                songs.extend(super().list_items(query=query + [('id','in',split_id)], limit = 25, LastEvaluatedKey=prevRecord, nextRecord = nextRecord))
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