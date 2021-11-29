import requests
from bs4 import BeautifulSoup 
import traceback
import re
headers = {'Authorization': 'Bearer ' + 'juoL7CJICtYLC5L2z-SpZPXL4sykzlPkvaxsFUlRFqM5dTaJe6rM7kB4p3A08zHH'}

def get_song_url(song_title, artist_name):
    try:
        base_url = 'https://api.genius.com'
        search_url = base_url + '/search'
        data = {'q': song_title + ' ' + artist_name}
        response = requests.get(search_url, params=data, headers=headers)
        resp_json = response.json()
        remote_song_info = None
        artist_name = artist_name.lower()
        for hit in resp_json['response']['hits']:
            condition = True
            for word in artist_name.split(' '):
                condition = condition and (word  in  hit['result']['primary_artist']['name'].lower())
            if condition:
                remote_song_info = hit['result']['url']
                break
        return remote_song_info
    except:
        print("error while fetching song url for song name {0} by {1}".format(song_title, artist_name))
        traceback.print_exc()
        raise

def get_lyrics_from_song_api_path(song_url):
    try:
        page = requests.get(song_url, headers=headers)
        html = BeautifulSoup(page.text, "html.parser")
        lyric_divs = html.find_all("div", attrs={"data-lyrics-container" : "true" })
        text = ""
        for lyric in lyric_divs:
            text += lyric.get_text(separator="\n")
        text = re.sub('\[(Verse [0-9]*|Chorus)\]', ' ', text)
        return text
    except:
        print("exception occured while fetching lyrics for url: {0}".format(song_url))
        traceback.print_exc()
        raise

def get_lyrics(song_title, artist_name):
        song_url = get_song_url(song_title, artist_name)
        if song_url == None:
            return song_url
        lyrics = get_lyrics_from_song_api_path(song_url)
        return lyrics
    

if __name__ == '__main__':
    song_name = input("Enter song name")
    artist_name = input("Enter artist name")
    print(get_lyrics(song_name, artist_name))