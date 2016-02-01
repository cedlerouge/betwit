from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Match(models.Model):
    """
    Match model
    """
    cup_round	= (
        ( '1', 'Round 1'),
        ( '2', 'Round 2'),
        ( '3', 'Round 3'),
        ( '4', 'Round 4'),
        ( '5', 'Round 5'),
    )

    teamA	= models.CharField( max_length=15)
    teamB	= models.CharField( max_length=15)
    match_date	= models.DateTimeField()
    cup_round	= models.CharField(max_length=1, choices=cup_round, default='1')
    scoreA      = models.IntegerField(null=True, blank=True)
    scoreB      = models.IntegerField(null=True, blank=True)
    triesA      = models.IntegerField(null=True, blank=True)
    triesB      = models.IntegerField(null=True, blank=True)
    card        = models.BooleanField(default=False)
    drop_goal   = models.BooleanField(default=False)
    fight       = models.BooleanField(default=False)
