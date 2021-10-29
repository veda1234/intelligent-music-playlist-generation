from django.shortcuts import render, redirect
from spotify.util import is_spotify_authenticated

# Create your views here.


def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

def index_with_authentication(request, *args, **kwargs):
    if is_spotify_authenticated(request.session.session_key):
        return render(request, 'frontend/index.html')
    return redirect('/')