from rest_framework import viewsets
from songs.models import Track
from rest_framework.response import Response
import traceback
import sys

class ArtistView(viewsets.ViewSet):
    def list(self, request, format=None):
        try:
            query_params = request.query_params.dict()
            prevId = None
            if 'prevId' in query_params:
                prevId = query_params['prevId']
                del query_params['prevId']
            songs = Track.get_songs(prevRecord = prevId)
            artist_responses = []
            for song in songs:
                song_response = song['artists'][0]
                song_response['track_id'] = song['id'] 
                artist_responses.append(song_response)
            return Response(artist_responses)
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

        