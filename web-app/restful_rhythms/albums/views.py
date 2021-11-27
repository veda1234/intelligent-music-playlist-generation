from rest_framework import viewsets
from .models import Album
from rest_framework.response import Response
import traceback
import sys

def format_album(album):
    artists = album.get("artists")
    if artists:
        artists = [artist.get("name") for artist in artists]
    else:
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
            query_params = request.query_params.dict()
            prevId = None
            if 'prevId' in query_params:
                prevId = query_params['prevId']
                del query_params['prevId']
            albums = Album.get_albums(prevRecord = prevId)
            album_responses = []
            for album in albums:
                album_responses.append(format_album(album))
            return Response(album_responses)
        except:
            print("some error occured while fetching albums")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)
        