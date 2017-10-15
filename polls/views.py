import os
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import F
from polls.models import Song, Vote

SPOTIFY_ID = os.environ['SPOTIFY_ID']
SPOTIFY_SECRET = os.environ['SPOTIFY_SECRET']

def index(request):
    return render(request, 'polls/index.html')

def vote_status(request, user_id):
    songs = list(Song.objects.filter(uid=user_id))
    return render(request, 'polls/status.html', {'songs': songs, 'user_id': user_id})

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
                              'redirect_uri': 'https://afternoon-plains-93869.herokuapp.com/auth',
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
                return redirect('/login', {'SPOTIFY_ID': SPOTIFY_ID})
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
                return redirect('/login', {'SPOTIFY_ID': SPOTIFY_ID})
            request.session['user_id'] = user['id']
            playlist = create_playlist(request)
            if create_playlist(request):
                messages.add_message(request, messages.SUCCESS, "Successfully authenticated with Spotify")
            else:
                messages.add_message(request, messages.ERROR, "Failed to create playlist - please log out and try again")
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, "Could not log in to Spotify: Got " + str(r.status_code))
            return redirect('/polls/login', {'SPOTIFY_ID': SPOTIFY_ID})

def vote(request, user_id):
    token = get_token()
    if token is None:
            messages.add_message(request, messages.ERROR, "Error getting token from Spotify, please try again later")
            return render(request, '/')
    return render(request, 'polls/vote.html', {'user_id': user_id, 'token': token})

def submit_vote(request, user_id):
    voter_email = request.POST.get('voter-email')
    song_id = request.POST.get('song-id')
    if Vote.objects.filter(email=voter_email, uid=user_id).exists():
        messages.add_message(request, messages.ERROR, "You cannot vote again until the next cycle!")
        return redirect('/polls')
    else:
        song_query = Song.objects.filter(sID=song_id, uid=user_id)
        if song_query.exists():
            song_query.update(votes=F('votes') + 1)
        else:
            token = get_token()
            if token is None:
                    messages.add_message(request, messages.ERROR, "Error getting token from Spotify, please try again later")
                    return render(request, '/')
            r = requests.get('https://api.spotify.com/v1/tracks/' + song_id,
                headers = {
                    'Authorization': 'Bearer ' + token
                }
            )
            if r.status_code != requests.codes.ok:
                    messages.add_message(request, messages.ERROR, "Spotify returned error " + r.status_code + ", please try again later")
                    return render(request, '/')
            rj = r.json()
            art_list = ', '.join(list(map(lambda x: x['name'], rj['artists'])))
            s = Song.objects.create(sID=song_id, name=rj['name'], album=rj['album']['name'], artists=art_list, votes = 1, uid=user_id)
        v = Vote.objects.create(email=voter_email, uid=user_id)
        messages.add_message(request, messages.SUCCESS, "Submitted your vote - come back for the next voting cycle later!")
        return redirect('/polls/' + user_id)

def call_vote(request, user_id):
    results = Song.objects.filter(uid=user_id).order_by('-votes')[:1].values_list('sID', flat=True)
    r = requests.post('https://api.spotify.com/v1/users/' + user_id + '/playlists/' + request.session['playlist_id'] + '/tracks',
                      json = {
                          'uris': list(map(lambda x: 'spotify:track:' + x, results))
                      },
                      headers = {
                          'Authorization': 'Bearer ' + request.session['access_token']
                      }
    )
    if r.status_code == requests.codes.created or r.status_code == requests.codes.ok:
        Song.objects.filter(uid=user_id).delete()
        Vote.objects.filter(uid=user_id).delete()
        messages.add_message(request, messages.SUCCESS, "Added songs to playlist!")
    else:
        messages.add_message(request, messages.ERROR, "Error adding songs to playlist, please try again")
    return redirect('/polls/' + user_id)

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

# Utility Methods
def create_playlist(request):
    u = request.session['user_id'] # user id string
    r = requests.post('https://api.spotify.com/v1/users/' + u + '/playlists',
        json = {
            'description': 'Playlist created automatically by Pollr!',
            'public': 'true',
            'name': 'Pollr Auto: ' + u
        },
        headers = {
            'Authorization': 'Bearer ' + request.session['access_token'],
            'Content-Type': 'application/json'
        }
    )
    if r.status_code == requests.codes.created:
        rj = r.json()
        request.session['playlist_id'] = rj['id']
        return True
    else:
        return False

def get_token():
    r = requests.post('https://accounts.spotify.com/api/token',
                      data = {
                          'grant_type': 'client_credentials',
                          'client_id': SPOTIFY_ID,
                          'client_secret': SPOTIFY_SECRET
                      },
    )
    if r.status_code == requests.codes.ok:
        try:
            response = r.json()
            token = response['access_token']
            return token
        except ValueError:
            return None
