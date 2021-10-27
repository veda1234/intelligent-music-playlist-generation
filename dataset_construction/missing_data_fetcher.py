import json
import os
from album_fetcher import AlbumDataManager
from track_fetcher import TrackDataManager
import pickle

MISSNG_ALBUM_PATH = '../dataset/missing_album_ids.pkl'
MISSNG_TRACK_PATH = '../dataset/missing_track_ids.pkl'


class DatasetManager:
    def __init__(self):
        self.album_data_manager = AlbumDataManager(prefix='missing_', use_id_file=False)
        self.track_data_manager = TrackDataManager(prefix='missing_', use_id_file=False)
    
    def process_missing_data(self):
        missing_album_ids = pickle.load(open(MISSNG_ALBUM_PATH, 'rb'))
        missing_track_ids = pickle.load(open(MISSNG_TRACK_PATH, 'rb'))
        print(len(missing_album_ids))
        print(len(missing_track_ids))
        for album_id in missing_album_ids:
            self.album_data_manager.add_album(album_id)
        for track_id in missing_track_ids:
            self.track_data_manager.add_track(track_id)
        self.album_data_manager.fetch_album_data(write_anyways=True)
        self.track_data_manager.fetch_track_data(write_anyways=True)
        
if __name__ == '__main__':
    dsm = DatasetManager()
    dsm.process_missing_data()