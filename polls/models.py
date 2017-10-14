from django.db import models

class Vote(models.Model):
    userSelection = False #user's default choice for a song is unselected
    email = models.CharField(max_length=200)
    voted_time = models.CharField(max_length=200)

class Song(models.Model):
    sID = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    artists = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)