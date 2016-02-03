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
    points_won		= models.IntegerField(null=True, blank=True)
    
