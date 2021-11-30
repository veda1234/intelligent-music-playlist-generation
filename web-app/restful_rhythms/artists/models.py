from common_utils import FirestoreModel
import traceback

class ArtistClass(FirestoreModel):
    def __init__(self):
        super(ArtistClass, self).__init__('artists')
    
    def get_artists_by_id(self, album_ids):
        try:
            albums = super().get_items_by_key(album_ids)
            return albums
        except:
            print("some error occured in fetching songs")
            traceback.print_exc()
            raise
    
    def get_artists(self,prevRecord = None, nextRecord = None, limit = 25):
        try:
            LastEvaluatedKey = None
            albums = super().list_items(limit = 25, LastEvaluatedKey=prevRecord, nextRecord = nextRecord)
            return albums
        except:
            print("some error occured in fetching songs")
            traceback.print_exc()
            raise


Artist = ArtistClass()