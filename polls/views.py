import os
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

SPOTIFY_ID = os.environ['SPOTIFY_ID']
SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']

def index(request):
    return render(request, 'polls/index.html')

def login(request):
    if request.session['access_token'] is not None:
        return redirect('/polls/')
    else:
        return render(request, 'polls/login.html', {'SPOTIFY_ID': SPOTIFY_ID})

def auth(request):
    code = request.GET.get('code')
    if code is None:
        error = request.GET.get('error')
        messages.add_message(request, messages.ERROR, "Could not log in to Spotify: " + error)
        return redirect('/polls', {'SPOTIFY_ID': SPOTIFY_ID})
    else:
        r = requests.post('https://accounts.spotify.com/api/token',
                          data = {
                              'grant_type': 'authorization_code',
                              'code': code,
                              'redirect_uri': 'http://localhost:8080/polls/auth',
                              'client_id': SPOTIFY_ID,
                              'client_secret': SPOTIFY_SECRET
                          },
        )
        if r.status_code == requests.codes.ok:
            response = ''
            try:
                response = r.json()
            except ValueError:
                messages.add_message(request, messages.ERROR, "Error getting token from Spotify, please try again")
                return render(request, 'polls/login.html', {'SPOTIFY_ID': SPOTIFY_ID})
            request.session['access_token'] = response['access_token']
            request.session['refresh_token'] = response['refresh_token']
            messages.add_message(request, messages.SUCCESS, "Successfully authenticated with Spotify")
            return redirect('/polls/index')
        else:
            messages.add_message(request, messages.ERROR, "Could not log in to Spotify: Got " + str(r.status_code))
            return redirect('/polls/login', {'SPOTIFY_ID': SPOTIFY_ID})

def search(request):
    return render(request, 'polls/search.html')

def voting(request):
    return render(request, 'polls/voting.html')
