import os
import requests
import random # I'm sorry
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
# Import(s) required for song search
from django.http import HttpResponseRedirect
from .forms import SongSearchForm

SPOTIFY_ID = os.environ['SPOTIFY_ID']
SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']

def caesarCipher(userName,randomInteger):
    for i in range(0:len(userName)-1):
        userName[i] = ord(userName[i]) + randomInteger
    return userName

def nameGen(userName):
    playlistName = 'Pollr Auto:'
    randNameExt = caesarCipher(userName,random.randint(1,13))
    playlistName = playlistName + randNameExt
    return playlistName

def create_playlist(request):
    u = requests.session[user_id] # user id string
    r = requests.post('https://api.spotify.com/v1/users/' + u + '/playlists/',
        data = {
            'description': 'Playlist created automatically by Pollr!',
            'public': True,
            'name': nameGen(u)
        }
    )

def song_search_form(request):
    # If this is a POST request we process the form data
    if request.method == 'POST':
        # Creates form instance and populates it with data from request
        form = SongSearchForm(request.POST)
        # Should implement some sort of validity checking here
        # Redirect to new URL
        return HttpResponseRedirect('/submit-results')
    # If a GET (or any other method) creates a blank form
    else:
        form = SongSearchForm()
    return render(request, 'SOMETHING ELSE GOES HERE.html', {'form': form})

def index(request):
    return render(request, 'polls/index.html')
    if request.session['access_token'] is not None:
        return render(request, 'polls/index.html', {'LOGGED_IN': True})
    else:
        return render(request, 'polls/index.html', {'LOGGED_IN': False})

def login(request):
    if request.session['access_token'] is not None:
        return redirect('/polls/')
    else:
        return render(request, 'polls/login.html', {'SPOTIFY_ID': SPOTIFY_ID})

def logout(request):
    request.session['access_token'] = None
    request.session['refresh_token'] = None
    messages.add_message(request, messages.SUCCESS, "Successfully logged out")
    return redirect('/polls/')

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
            profile = requests.get('https://api.spotify.com/v1/me',
                                   headers = {
                                       'Authorization': "Bearer {}".format(request.session['access_token'])
                                   })
            try:
                user = profile.json()
            except ValueError:
                messages.add_message(request, messages.ERROR, "Error getting user id, please try again")
                return render(request, 'polls/login.html', {'SPOTIFY_ID': SPOTIFY_ID})
            request.session['user_id'] = user['id']
            messages.add_message(request, messages.SUCCESS, "Successfully authenticated with Spotify")
            return redirect('/polls/')
        else:
            messages.add_message(request, messages.ERROR, "Could not log in to Spotify: Got " + str(r.status_code))
            return redirect('/polls/login', {'SPOTIFY_ID': SPOTIFY_ID})

def search(request):
    return render(request, 'polls/search.html')

def vote(request, user_id):
    return render(request, 'polls/vote.html', {'user_id': user_id})

# Context Processors
def spotify_session(request):
    if request.session['access_token'] is not None:
        context = {
            'logged_in': True,
            'user': request.session['user_id']
        }
    else:
        context = {'logged_in': False}
    return context
