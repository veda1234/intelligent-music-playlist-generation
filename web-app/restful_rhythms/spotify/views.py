from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import update_or_create_user_tokens, is_spotify_authenticated, execute_spotify_api_request
from songs.models import Track

class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url
        
        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('harmonic_ui:welcome')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

class SearchView(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        if not is_authenticated:
            return Response({'error' : 'not authenticated' }, status=status.HTTP_401_UNAUTHORIZED)
        query_params = request.query_params.dict()
        if 'search' not in query_params:
            return Response({"error": "search query should be provided in search param"}, status=400) 
        spotify_search_params = {
            'q': query_params['search'],
            'type': 'track',
            'limit': 25,
        }
        if 'page_number' in query_params:
            spotify_search_params['offset'] = 25*(int(query_params['page_number']) - 1)
        response = execute_spotify_api_request(self.request.session.session_key, '/search',spotify_search_params)
        tracks = response['tracks']['items']
        track_ids = [track['id'] for track in tracks]
        track_id_sets = chunks(track_ids, 10)
        present_Tracks = []
        for track_id_set in track_id_sets:
            present_Tracks.extend(Track.get_songs(query_params={ 'id' : track_id_set }))
        present_Track_set = set([track['id'] for track in present_Tracks])
        for track in tracks:
            track['is_already_present'] = (track['id'] in present_Track_set)
        return Response(response['tracks']["items"])
