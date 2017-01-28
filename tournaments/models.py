from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Team(models.Model):
    """
    Team model
    """
    name        = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    logo        = models.ImageField(upload_to=settings.IMAGE_UPLOAD_PATH)
    thumbnail   = models.ImageField(upload_to=settings.THUMBNAIL_UPLOAD_PATH)

class Tournament(models.Model):
    """
    Tournament model
    """
    name        = models.CharField(max_length=20)
    year        = models.IntegerField()

class Match(model.Model):
    """
    Match model
    """
    bonus = ("Defense", "Attack")

    tournament_id   = models.ForeignKey(Tournament)
    date            = models.DateTimeField(auto_now_add=False)
    #tournament_round = models.IntegerField()
    home_team_id    = models.IntegerField()
    home_team_score = models.IntegerField()
    home_team_tries = models.IntegerField()
    home_team_bonus = models.CharField(max_length=15, choices=bonus, default='--')
    home_team_point = models.IntegerField() 
    away_team_id    = models.IntegerField()
    away_team_score = models.IntegerField()
    away_team_tries = models.IntegerField() 
    away_team_bonus = models.CharField(max_length=15, choices=bonus, default='--')    
    away_team_point = models.IntegerField() 
    card            = models.BooleanField(default=False)
    drop_goal       = models.BooleanField(default=False)
    fight           = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now_add=True)
    points_won      = models.IntegerField(null=True, blank=True, default=0)
    comment         = models.CharField( max_length=1000 )

class MatchPoint(models.Model):                     
    """                                           
    MatchPoint model is a key/value table that store
    - each element of match as key                  
    - each point of winning element as value      
    - risk let to know if there is netgative point (risk = True) or not (risk = False)
    """                                           
    key             = models.CharField()
    value           = models.IntegerField()
    risk            = models.BooleanField(default=False)
