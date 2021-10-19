import os
import pickle
import json 


PLAYLIST_PATH = '../dataset/data/'
ALBUM_DATA_PATH = '../dataset/albums'
TRACK_DATA_PATH = '../dataset/tracks'

ALBUM_ID_PATH = '../dataset/missing_album_ids.pkl'
TRACK_ID_PATH = '../dataset/missing_track_ids.pkl'


def create_unique_ids(filepath):
    unique_ids = set()
    files = os.listdir(filepath)
    clean_json = []
    for file in files:
        if file.startswith("clean"):
            object_array = json.load(open(filepath + '/' + file, 'r'))
            for obj in object_array:
                unique_ids.add(obj["id"])
    return unique_ids 

def verify_file(filepath, album_ids, track_ids):
    not_present_tracks = []
    not_present_albums = []
    object_array = json.load(open(filepath, 'r'))
    for obj in object_array["playlists"]:
        for track in obj["tracks"]:
            track_id = track["track_uri"].split(":")[-1]
            album_id = track["album_uri"].split(":")[-1]
            if track_id not in track_ids:
                not_present_tracks.append(track_id)
            if album_id not in album_ids:
                not_present_albums.append(album_id)
    # if len(not_present_albums) > 0 or len(not_present_tracks) > 0:
    #     print("some data is missing in the file {0}".format(filepath))
    #     print("not present albums: {0}".format(not_present_albums))
    #     print("not present tracks: {0}".format( not_present_tracks))
    return not_present_albums, not_present_tracks        

def verify_dataset(album_ids, track_ids):
    files = os.listdir(PLAYLIST_PATH)
    i = 0
    not_present_albums = set()
    not_present_tracks = set()
    for file in files:
        npa, npt = verify_file(PLAYLIST_PATH + file, album_ids, track_ids)
        not_present_albums = not_present_albums.union(set(npa))
        not_present_tracks =  not_present_tracks.union(set(npt))
        i += 1
        if i % 10 == 0:
            print(len(not_present_tracks))
            print(len(not_present_albums))
            print('{0} done'.format(i))
    o_file = open(ALBUM_ID_PATH, 'wb')
    pickle.dump(not_present_albums, o_file)
    o_file.close()
    o_file = open(TRACK_ID_PATH, 'wb')
    pickle.dump(not_present_tracks, o_file)
    o_file.close()
        

if __name__ == '__main__':
    album_ids = create_unique_ids(ALBUM_DATA_PATH)
    track_ids = create_unique_ids(TRACK_DATA_PATH)
    verify_dataset(album_ids, track_ids)