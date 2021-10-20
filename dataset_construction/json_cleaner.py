import os
import json

ALBUM_DATA_PATH = '../dataset/albums'
TRACK_DATA_PATH = '../dataset/tracks'


def write_json(filepath, prefix, clean_json):
    filenames = os.listdir(filepath)
    filenames = [fi for fi in filenames if fi.startswith('clean')]
    new_num = len(filenames) + 1
    out_f = open(filepath + '/clean_{0}_{1}.json'.format(prefix, new_num), 'w')
    out_f.write(json.dumps(clean_json, indent=4))
    out_f.close()

def create_clean_json(filepath, prefix):
    unique_ids = set()
    files = os.listdir(filepath)
    clean_json = []
    for file in files:
        object_array = json.load(open(filepath + '/' + file, 'r'))
        for obj in object_array:
            if obj["id"] not in unique_ids:
                print(obj["id"])
                clean_json.append(obj)
                unique_ids.add(obj["id"])
            if len(clean_json) == 5000:
                write_json(filepath, prefix, clean_json)
                clean_json = []
            
            

if __name__ == '__main__':
    create_clean_json(ALBUM_DATA_PATH,'album')
    create_clean_json(TRACK_DATA_PATH,'track')
    