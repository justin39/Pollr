from django.db import models

class Vote(models.Model):
    userSelection = False #user's default choice for a song is unselected
    email = ''
    voted_time = ''


class Song(models.Model): 