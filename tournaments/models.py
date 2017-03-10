from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.

class Team(models.Model):
    """
    Team model
    """
    name        = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
#    logo        = models.ImageField(upload_to=settings.IMAGE_UPLOAD_PATH)
#    thumbnail   = models.ImageField(upload_to=settings.THUMBNAIL_UPLOAD_PATH)

    def __str__(self):
        return self.name

class Tournament(models.Model):
    """
    Tournament model
    """
    state_choice = (
        ("1", "Enabled"),
        ("2", "Comming"),
        ("3", "Archived")
    )

    name        = models.CharField(max_length=20)
    year        = models.IntegerField()
    begins      = models.DateTimeField()
    state       = models.CharField(max_length=1, choices=state_choice, default='2')

    def __str__(self):
        return self.name + " - " + str(self.year)

class Match(models.Model):
    """
    Match model
    """
    bonus = (
        ('Null', "Null"),
        ("Defense","Defense"), 
        ("Attack","Attack")
    )
    cup_round   = (
        ( '1', 'Round 1'),
        ( '2', 'Round 2'),
        ( '3', 'Round 3'),
        ( '4', 'Round 4'),
        ( '5', 'Round 5'),
    )


    tournament_id   = models.ForeignKey( Tournament )
    date            = models.DateTimeField( auto_now_add=False )
    cup_round       = models.CharField(max_length=1, choices=cup_round, default='1')
    #tournament_round = models.IntegerField()
    home_team_id    = models.ForeignKey(Team, related_name="home_team" )
    home_team_score = models.IntegerField( null=True, blank=True )
    home_team_tries = models.IntegerField( null=True, blank=True )
    home_team_bonus = models.CharField( max_length=15, choices=bonus, default='--' )
    home_team_point = models.IntegerField( null=True, blank=True ) 
    away_team_id    = models.ForeignKey( Team, related_name="away_team" )
    away_team_score = models.IntegerField( null=True, blank=True )
    away_team_tries = models.IntegerField( null=True, blank=True ) 
    away_team_bonus = models.CharField( max_length=15, choices=bonus, default='--' )    
    away_team_point = models.IntegerField( null=True, blank=True ) 
    card            = models.BooleanField( default=False )
    drop_goal       = models.BooleanField( default=False )
    fight           = models.BooleanField( default=False )
    created_date    = models.DateTimeField( auto_now_add=True )
    modified_date   = models.DateTimeField( auto_now_add=True )
    points_won      = models.IntegerField( null=True, blank=True, default=0 )
    odds            = models.IntegerField( null=True, blank=True, default=0 )
    comment         = models.TextField( max_length=1000, null=True, blank=True )

    def __unicode__(self):
        return "%s vs %s" % (self.home_team_id, self.away_team_id)

class MatchPoint(models.Model):                     
    """                                           
    MatchPoint model is a key/value table that store
    - each element of match as key                  
    - each point of winning element as value      
    - risk let to know if there is netgative point (risk = True) or not (risk = False)
    """                                           
    key             = models.CharField(max_length=200)
    value           = models.IntegerField()
    risk            = models.BooleanField(default=False)
