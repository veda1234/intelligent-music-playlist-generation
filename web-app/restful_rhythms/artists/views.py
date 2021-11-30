from rest_framework import viewsets
from .models import Artist
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
            nextId = None
            if 'nextId' in query_params:
                nextId = query_params['nextId']
                del query_params['nextId']
            artists = Artist.get_artists(prevRecord = prevId, nextRecord = nextId)
            return Response(artists)
        except:
            print("some error occured while fetching songs")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)
        
    def retrieve(self, request, pk=None):
        try:
            is_authenticated = is_spotify_authenticated(
                self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
            artist = Artist.get_item(pk)
            if artist == None:
                return Response({"error": "artist not found" }, status=404)
            return Response(artist)
        except:
            print(f"some error occured while fetching song for id {pk}")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)
