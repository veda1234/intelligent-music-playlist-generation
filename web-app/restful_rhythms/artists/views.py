from rest_framework import viewsets
from songs.models import Track, UserTrack
from rest_framework.response import Response
import traceback
import sys

def format_song(song, albums):
    artists = song.get("artists")
    for artist in artists:
        artist["song_id"] = 
    else:
        artists = []
    duration = song.get("duration")
    duration_dict = {}
    if duration:
        duration_seconds = round(duration / 1000)
        duration_minutes  = duration_seconds // 60
        duration_hours = duration_minutes // 60
        duration_seconds = duration_seconds % 60
        duration_minutes = duration_minutes % 60
        duration_dict = {
            'minutes' : duration_minutes,
            'hours' : duration_hours,
            'seconds' : duration_seconds
        }
    song_response = {
        "name": song.get("name"),
        "id": song.get("id"),
        "artists": artists,
        "duration_minutes": duration_dict.get('minutes'),
        "duration_seconds": duration_dict.get('seconds'),
        "duration_hours": duration_dict.get('hours'),
        "preview_url": song.get('preview_url'),
        "cluster": song.get('cluster'),
        "emotion": song.get('emotion')
    }
    if albums.get(song.get('album_id')):
        song_response["album"] = albums.get(song.get("album_id")).get("name"),
    return song_response

class SongView(viewsets.ViewSet):
    def list(self, request, format=None):
        try:
            query_params = request.query_params.dict()
            prevId = None
            if 'prevId' in query_params:
                prevId = query_params['prevId']
                del query_params['prevId']
            for q in query_params:
                if q in ['cluster','emotion']:
                    query_params[q] = query_params[q][1:-1].split(',')
                if q == 'cluster':
                    query_params[q] = [int(val) for val in query_params[q]]
                if q == 'user_id':
                    song_ids = UserTrack.get_user_songs(query_params[q])
                    del query_params[q]
                    query_params['id'] = song_ids
            songs = Track.get_songs(query_params=query_params, prevRecord = prevId)
            song_responses = []
            album_ids = [song.get("album_id") for song in songs]
            albums = Album.get_albums_by_id(album_ids)
            for song in songs:
                song_responses.append(format_song(song, albums))
            return Response(song_responses)
        except:
            print("some error occured while fetching songs")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)
    
    def retrieve(self, request, pk=None):
        try:
            song = Track.get_item(pk)
            if song == None:
                return Response({"error": "song not found" }, status=404)
            albums = {}
            album_id = song.get('album_id')
            if album_id:
                album = Album.get_item(album_id)
                if album:
                    albums[album['id']] = album
            song_data = format_song(song, albums)
            song_feature_data = TrackFeatures.get_track_features(song.get('id'))
            if song_feature_data:
                song_data['audio_features'] = song_feature_data.get('audio_features')
                song_data['lyrics'] = song_feature_data.get('lyrics')
            return Response(song_data)
        except:
            print(f"some error occured while fetching song for id {pk}")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)

        