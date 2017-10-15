from django.db import models

class Vote(models.Model):
    email = models.CharField(max_length=200)
    voted_time = models.DateTimeField(auto_now_add=True)
    uid = models.CharField(max_length=200)

class Song(models.Model):
    sID = models.CharField(max_length=200) # spotify ID
    name = models.CharField(max_length=200)
    artists = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)
    uid = models.CharField(max_length=200)
