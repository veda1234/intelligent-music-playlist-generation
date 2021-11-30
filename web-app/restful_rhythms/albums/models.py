from common_utils import FirestoreModel
import traceback

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

class AlbumClass(FirestoreModel):
    def __init__(self):
        super(AlbumClass, self).__init__('albums')
    
    def get_albums_by_id(self, album_ids):
        try:
            id_chunks = chunks(album_ids, 10)
            albums = {}
            for ch in id_chunks:
                new_albums = super().get_items_by_key(ch)
                for album in new_albums:
                    albums[album] = new_albums[album]
            return albums
        except:
            print("some error occured in fetching songs")
            traceback.print_exc()
            raise
    
    def get_albums(self,prevRecord = None, nextRecord = None, limit = 25):
        try:
            LastEvaluatedKey = None
            albums = super().list_items(limit = 25, LastEvaluatedKey=prevRecord, nextRecord = nextRecord)
            return albums
        except:
            print("some error occured in fetching songs")
            traceback.print_exc()
            raise


Album = AlbumClass()