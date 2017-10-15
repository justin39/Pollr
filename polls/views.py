from django.shortcuts import render
from django.http import HttpResponse
# Import(s) required for song search
from django.http import HttpResponseRedirect
from .forms import SongSearchForm

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

def search(request):
    return render(request, 'polls/search.html')

def voting(request):
    return render(request, 'polls/voting.html')