from common_utils import DynamoModel
import traceback

class AlbumClass(DynamoModel):
    def __init__(self):
        super(AlbumClass, self).__init__('albums')
    
    def get_albums_by_id(self, album_ids):
        try:
            albums = super().get_items_by_key(album_ids)
            return albums
        except:
            print("some error occured in fetching songs")
            traceback.print_exc()
            raise

Album = AlbumClass()