import requests
from bs4 import BeautifulSoup
import pickle
import re
import json
import os
import traceback

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer juoL7CJICtYLC5L2z-SpZPXL4sykzlPkvaxsFUlRFqM5dTaJe6rM7kB4p3A08zHH'}

TRACK_DATA_PATH = '../dataset/clean_tracks'
TRACK_URL_PATH = '../dataset/track_lyric_urls.pkl'
TRACK_LYRICS_PATH = '../dataset/lyrics'

def lyrics_from_song_api_path(song_url):
    page = requests.get(song_url, headers=headers)
    # json = response.json()
    # path = json["response"]["song"]["path"]
    # page_url = "http://genius.com" + path
    # page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    lyric_divs = html.find_all("div", attrs={"data-lyrics-container" : "true" })
    text = ""
    for lyric in lyric_divs:
        text += lyric.get_text(separator="\n")
    text = re.sub('\[(Verse [0-9]*|Chorus)\]', ' ', text)
    return text

def write_lyrics(lyric_map, suffix):
    filename = TRACK_LYRICS_PATH + '/lyrics_{0}.json'.format(suffix)
    if os.path.exists(filename):
        lyric_old_json = json.load(open(filename,'r'))
        for key in lyric_old_json:
            lyric_map[key] = lyric_old_json[key]
    json.dump(lyric_map, open(filename, 'w'))

if __name__ == "__main__":
    track_urls = pickle.load(open(TRACK_URL_PATH, 'rb'))
    count = 0
    tot_count = 0
    for key in track_urls:
        if track_urls[key] != None:
          count += 1
        tot_count += 1
    print("lyric available for {0} songs out of {1} songs".format(count, tot_count))
    point_reached = False
    lyric_map = {}
    last_key = '1U4jkbfzoAQRc7qrGhrrUQ'
    for i, key in enumerate(track_urls):
        try:
            if key == last_key:
                point_reached = True
            if not point_reached:
                continue
            if track_urls[key] != None:
                lyrics = lyrics_from_song_api_path(track_urls[key])
                lyric_map[key] = lyrics
            if i % 1000 == 999:
                write_lyrics(lyric_map, i)
                lyric_map = {}
            if i % 100 == 0:
                print(len(lyric_map))
                print("{0} done".format(i))
        except:
            print("error at track key: {0}".format(key))
            traceback.print_exc()
            write_lyrics(lyric_map,i)
            raise
    write_lyrics(lyric_map, tot_count)
