from django import forms

class SongSearchForm(forms.Form):
    song_name = forms.CharField(max_length=200, initial='Fuckboi')
    artist_name = forms.CharField(max_length=200, initial='AJJ')