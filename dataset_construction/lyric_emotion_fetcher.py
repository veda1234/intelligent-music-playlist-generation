import pickle
import traceback
import os
import json
import sys
sys.path.append('../')

from lyric_emotion_detection.emotion_fetcher import get_lyric_emotion

LYRIC_PATH = '../dataset/lyrics'
TRACK_EMOTION_PATH = '../dataset/track_lyric_emotions.pkl'


def get_data_for_lyrics_file(file, st_index=0):
    global track_emotions
    filename = LYRIC_PATH + '/' + file
    lyric_map = json.load(open(filename, 'r'))
    for i,track_id in enumerate(lyric_map):
        try:
            track_emotions[track_id] = get_lyric_emotion(lyric_map[track_id])
            # print(track_emotions[track_id])
        except:
            print("error at track index: {0} for song id {1}".format(st_index + i,track_id))
            traceback.print_exc()
            raise

    
if __name__ == '__main__':
    global track_emotions   
    track_emotions = {}     
    files = sorted(os.listdir(LYRIC_PATH))
    i = 0
    if os.path.exists(TRACK_EMOTION_PATH):
        track_emotions = pickle.load(open(TRACK_EMOTION_PATH, 'rb'))
    print(len(files))
    for file in files:
        try:
            if i == 0:
                get_data_for_lyrics_file(file, 0)
            else:
                get_data_for_lyrics_file(file)
            if i % 10 == 9:
                print('{0} th file done'.format(i+1))
            i += 1
        except:
            print("error at lyric file index: {0}".format(i))
            traceback.print_exc()
            pickle.dump(track_emotions, open(TRACK_EMOTION_PATH, 'wb'))
            raise
    pickle.dump(track_emotions, open(TRACK_EMOTION_PATH, 'wb'))
