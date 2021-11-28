from rest_framework import viewsets
from songs.models import Track
from rest_framework.response import Response
import traceback
import sys
from spotify.util import is_spotify_authenticated
from rest_framework import status

class ArtistView(viewsets.ViewSet):
    def list(self, request, format=None):
        try:
            is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
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