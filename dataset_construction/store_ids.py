import os
import json
import pickle
import sys

def process_mpd(path):
    count=0
    test_ids = set()
    filenames = os.listdir(path)
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            f = open(fullpath)
            js = f.read()
            f.close()
            mpd_slice = json.loads(js)
            process_info(mpd_slice["info"])
            for playlist in mpd_slice["playlists"]:
                get_tracks = playlist["tracks"]
                for tracks in get_tracks:
                    if tracks['track_uri'].split(':')[2] not in test_ids:
                        test_ids.add(tracks['track_uri'].split(':')[2])
                        count+=1
    with open('store_ids.pickle', 'wb') as f:
        pickle.dump(test_ids,f)

def process_info(_):
    pass

if __name__ == '__main__':
    path = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--quick":
        quick = True
    track_ids = process_mpd(path)