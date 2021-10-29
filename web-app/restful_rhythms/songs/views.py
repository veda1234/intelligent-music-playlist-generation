from rest_framework import viewsets
from .models import Track
from rest_framework.response import Response
import traceback

class SongView(viewsets.ViewSet):
    def list(self, request, format=None):
        try:
            songs = Track.get_songs()
            song_responses = []
            for song in songs:
                artists = song.get("artists")
                if artists:
                    artists = [artist.get("name") for artist in artists]
                else:
                    artists = []
                duration = song.get("duration")
                if duration:
                    duration_seconds = round(duration / 1000)
                    duration_minutes  = duration_seconds // 60
                    duration_hours = duration_minutes // 60
                    duration_seconds = duration_seconds % 60
                    duration_minutes = duration_minutes % 60
                song_responses.append({
                    "name": song.get("name"),
                    "id": song.get("id"),
                    "artists": artists,
                    "duration_minutes": duration_minutes,
                    "duration_seconds": duration_seconds,
                    "duration_hours": duration_hours,
                    "album": song.get("album_id"),
                    "preview_url": song["preview_url"]
                })
            return Response(song_responses)
        except:
            print("some error occured while fetching songs")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)

        