from rest_framework import viewsets
from .models import Album
from rest_framework.response import Response
import traceback
import sys
from spotify.util import is_spotify_authenticated
from rest_framework import status

def format_album(album):
    artists = album.get("artists")
    if not artists:
        artists = []
    album_response = {
        "name": album.get("name"),
        "id": album.get("id"),
        "artists": artists,
        "release_date": album.get("release_date"),
        "release_date_precision": album.get("release_date_precision"),
    }
    return album_response
class AlbumView(viewsets.ViewSet):
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
            albums = Album.get_albums(prevRecord = prevId, nextRecord = nextId)
            album_responses = []
            for album in albums:
                album_responses.append(format_album(album))
            return Response(album_responses)
        except:
            print("some error occured while fetching albums")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)
    
    def retrieve(self, request, pk=None):
        try:
            is_authenticated = is_spotify_authenticated(
                self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
            album = Album.get_item(pk)
            if album == None:
                return Response({"error": "album not found" }, status=404)
            return Response(album)
        except:
            print(f"some error occured while fetching song for id {pk}")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)