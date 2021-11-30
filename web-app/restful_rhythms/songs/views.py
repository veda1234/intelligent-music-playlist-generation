from rest_framework import viewsets
from .models import Track, UserTrack
from albums.models import Album
from song_features.models import TrackFeatures 
from rest_framework.response import Response
from rest_framework.decorators import action
import traceback
import sys
from spotify.util import is_spotify_authenticated, execute_spotify_api_request
from rest_framework import status
sys.path.append('../../')
from lyric_emotion_detection import emotion_fetcher
from cluster_detection import get_user_cluster_ids
import json


def add_song_to_user(session_id, track_id):
    curr_user_data = execute_spotify_api_request(session_id, '/me')
    user_id = curr_user_data['id']
    user_tracks = UserTrack.get_item(user_id)
    if not user_tracks:
        user_tracks = {
            'songs': [],
            'user_id': user_id,
        }
    if track_id not in user_tracks['songs']:
        user_tracks['songs'].append(track_id)
    UserTrack.write_item(user_tracks)

def format_song(song, albums):
    artists = song.get("artists")
    if artists:
        artists = [artist.get("name") for artist in artists]
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

def construct_song(song):
    artists = song.get("artists")
    if artists:
        artists = [{ 'name': artist['name'], 'id': artist['id'] } for artist in artists]
    else:
        artists = []
    song_response = {
        "name": song.get("name"),
        "id": song.get("id"),
        "artists": artists,
        "duration": song.get("duration_ms"),
        "preview_url": song.get('preview_url'),
        "popularity": song.get('popularity'),
        "album_id": song['album']['id'],
    }
    album = song['album']
    album_artists = album.get('artists')
    if album_artists:
        album_artists = [{ 'name': album_artist['name'],
                            'id': album_artist['id'] } for album_artist in album_artists]
    else:
        artists = []
    album_response = {
        "name": album.get('name'),
        "id": album.get('id'),
        "release_date": album.get('release_date'),
        "release_date_precision": album.get('release_date_precision'),
        "album_type": album.get('type'),
        "artists": album.get('album_artists'),
    }
    return song_response, album_response

class SongView(viewsets.ViewSet):
    def list(self, request, format=None):
        try:
            is_authenticated = is_spotify_authenticated(
                self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
            query_params = request.query_params.dict()
            prevId = None
            nextId = None
            if 'prevId' in query_params:
                prevId = query_params['prevId']
                del query_params['prevId']
            elif 'nextId' in query_params:
                nextId = query_params['nextId']
                del query_params['nextId']
            param_keys = list(query_params.keys())
            for q in param_keys:
                if q == 'cluster':
                    query_params[q] = int(query_params[q])
                if q == 'emotion':
                    query_params[q] = query_params[q].lower()
                if q == 'by_user':
                    curr_user_data = execute_spotify_api_request(request.session.session_key, '/me')
                    user_id = curr_user_data['id']
                    song_ids = UserTrack.get_user_songs(user_id)
                    del query_params['by_user']
                    query_params['id'] = song_ids  
            songs = Track.get_songs(query_params=query_params, prevRecord = prevId, nextRecord=nextId)
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
            is_authenticated = is_spotify_authenticated(
                self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
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
    
    def create(self, request):
        try:
            is_authenticated = is_spotify_authenticated(
                self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED) 
            request_data = request.data
            if 'track_id' not in request_data:
                return Response({"error": "track id should be provided" }, status=400)
            track_id = request_data['track_id']
            track_response = execute_spotify_api_request(request.session.session_key, f'/tracks/{track_id}')
            if 'error' in track_response:
                return Response({"error": "track id not found" }, status=404)
            song_response, album_response = construct_song(track_response)
            lyrics = None
            if song_response.get('name') and song_response.get('artists'):
                name = song_response['name']
                artist_name = song_response['artists'][0]['name']
                data = emotion_fetcher.get_song_emotion(name, artist_name)
                if data:
                    song_response['emotion'] = data['emotion']
                    lyrics = { 'id': track_id, 'lyrics': data['lyrics'] }  
            audio_features = None
            audio_feature_response = execute_spotify_api_request(
                request.session.session_key,f'/audio-features', { 'ids': track_id })
            if 'audio_features' in audio_feature_response and len(audio_feature_response['audio_features']) > 0:
                audio_features = audio_feature_response['audio_features'][0]
                del audio_features['type']
                del audio_features['uri']
                del audio_features['track_href']
                del audio_features['analysis_url']
                song_response['cluster'] = get_user_cluster_ids.get_user_audio_features(audio_features)
            Track.write_item(song_response)
            Album.write_item(album_response)
            if lyrics and audio_features:
                lyrics['audio_features'] = audio_features
            if lyrics:
                TrackFeatures.write_item(lyrics)
            add_song_to_user(request.session.session_key, track_id) 
            return Response("success")
        except:
            print(f"some error occured while creating song for {request.data}")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)   

    @action(detail=False, methods=['post'])
    def add_to_list(self, request):
        try:
            is_authenticated = is_spotify_authenticated(
                    self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
            if 'track_id' not in request.data:
                return Response({'error': 'track_id not given' }, status=status.HTTP_400_BAD_REQUEST)
            add_song_to_user(request.session.session_key, request.data['track_id'])
            return Response("success")
        except:
            print(f"some error occured while adding song to user for {request.data}")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)
    

    @action(detail=False,methods=['post'], name='export')
    def export(self,request):
        try:
            is_authenticated = is_spotify_authenticated(
                    self.request.session.session_key)
            if not is_authenticated:
                return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
            session_id = request.session.session_key
            curr_user_data = execute_spotify_api_request(session_id, '/me')
            user_id = curr_user_data['id']
            query_params = request.data
            response = execute_spotify_api_request(session_id, f'/users/{user_id}/playlists',
                { 'name': query_params.get('name')},post_=True)
            if 'error' in response:
                return Response({'error': 'cannot create playlist' },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            playlist_id = response['id']
            track_uris = []
            for track_id in query_params['track_ids']:
                track_uris.append(f'spotify:track:{track_id}')
            response = execute_spotify_api_request(session_id,f'/playlists/{playlist_id}/tracks',
                { 'uris': track_uris }, post_=True)
            if 'error' in response:
                return Response({'error': 'cannot add tracks' },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response('sucess')
        except:
            print(f"some error occured while exporting songs for {request.query_params.dict()}")
            print(traceback.print_exc())
            return Response({"error" : traceback.format_exc() }, status=500)
        