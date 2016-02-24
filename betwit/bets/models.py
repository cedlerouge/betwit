from __future__ import unicode_literals

from django.db import models

# Create your models here.

from user_profile.models import User
from matchs.models import Match

class Bet(models.Model):
    """
    Bets model
    """
    user		= models.ForeignKey(User)
    match		= models.ForeignKey(Match)
    scoreA		= models.IntegerField()
    scoreB		= models.IntegerField()
    triesA		= models.IntegerField()
    triesB		= models.IntegerField()
    card		= models.BooleanField(default=False)
    drop_goal		= models.BooleanField(default=False)
    fight	     	= models.BooleanField(default=False)
    created_date	= models.DateTimeField(auto_now_add=True)
    modified_date	= models.DateTimeField(auto_now_add=True)
    points_won		= models.IntegerField(null=True, blank=True, default=0)
    

class BetCup(models.Model):
    """
    BetCup - bet on final rank in the cup
    """
    teams = (
      ('an', 'Angleterre'),
      ('ec', 'Ecosse'),
      ('fr', 'France'),
      ('ir', 'Irelande'),
      ('it', 'Italie'),
      ('pg', 'Pays de Galles'),
    )
    

    user		= models.ForeignKey(User)
    first		= models.CharField(max_length=15, choices=teams, default='--')
    second              = models.CharField(max_length=15, choices=teams, default='--')
    third               = models.CharField(max_length=15, choices=teams, default='--')
    fourth              = models.CharField(max_length=15, choices=teams, default='--')
    fifth               = models.CharField(max_length=15, choices=teams, default='--')
    sixth               = models.CharField(max_length=15, choices=teams, default='--')
    grand_slam		= models.BooleanField(default=False)
    wooden_spoon	= models.BooleanField(default=False)
    points_won		= models.IntegerField(null=True, blank=True)
    created_date	= models.DateTimeField(auto_now_add=True)
