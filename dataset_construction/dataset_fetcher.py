import json
import os
from album_fetcher import AlbumDataManager
from track_fetcher import TrackDataManager

PLAYLIST_PATH = '../dataset/data'

class DatasetManager:
    def __init__(self):
        self.album_data_manager = AlbumDataManager()
        self.track_data_manager = TrackDataManager()
    
    
    def process_file(self, filename):
        data_dict = json.load(open(PLAYLIST_PATH + '/' + filename, 'r'))
        playlists = data_dict['playlists']
        for playlist in playlists:
            tracks = playlist["tracks"]
            for track in tracks:
                # album process
                album_id = track["album_uri"].split(':')[-1]
                self.album_data_manager.add_album(album_id)

                # track process
                track_id = track["track_uri"].split(':')[-1]
                self.track_data_manager.add_track(track_id)
                
        self.album_data_manager.fetch_album_data(write_anyways=True)
        self.track_data_manager.fetch_track_data(write_anyways=True)

        
if __name__ == '__main__':
    files = os.listdir(PLAYLIST_PATH)
    print(len(files))
    i = 0
    dsm = DatasetManager()
    for file in files:
        dsm.process_file(file)
        print('{0} done'.format(file))
        i += 1
        if i % 100 == 0:
            print('{0} done'.format(i))
    