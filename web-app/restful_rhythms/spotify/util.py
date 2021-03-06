from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get
import json


BASE_URL = "https://api.spotify.com/v1/me/"
SPOTIFY_BASE_URL = 'https://api.spotify.com/v1'


def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        update_fields = ['access_token', 'expires_in', 'token_type']
        if refresh_token:
            tokens.refresh_token = refresh_token
            update_fields.append('refresh_token')
        tokens.save(update_fields=update_fields)
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        return True

    return False


def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()
    print(response)
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token)

def execute_spotify_api_request(session_id, endpoint, query_params = {}, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}
    if post_:
        response = post(SPOTIFY_BASE_URL + endpoint,data=json.dumps(query_params),headers=headers)
    elif put_:
        response = put(SPOTIFY_BASE_URL + endpoint, headers=headers)
    else:
        response = get(SPOTIFY_BASE_URL + endpoint, query_params, headers=headers)
    try:
        return response.json()
    except:
        print(response)
        print(endpoint)
        print(query_params)
        return {'Error': 'Issue with request'}