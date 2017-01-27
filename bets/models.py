from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Match, Tournament


# Create your models here.

class MatchBet(models.Model):
    """
    Bets model : one bet per match and per player
    """
    palyer_id       = models.ForeignKey(User)
    match_id        = models.ForeigneKey(Match)
    home_team_score = models.IntegerField()
    home_team_tries = models.IntegerField()
    home_team_bonus = models.IntegerField()
    away_team_score = models.IntegerField()
    away_team_tries = models.IntegerField()
    away_team_bonus = models.IntegerField()
    card            = models.BooleanField(default=False)
    drop_goal       = models.BooleanField(default=False)
    fight           = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now_add=True)
    points_won      = models.IntegerField(null=True, blank=True, default=0)

class TournamentBet(models.Model):
    """
    Tournament Bets model : one bet per player
    """

    # TODO rendre cette list dynamique 
    teams = (
      ('an', 'Angleterre'),
      ('ec', 'Ecosse'),
      ('fr', 'France'),
      ('ir', 'Irlande'),
      ('it', 'Italie'),
      ('pg', 'Pays de Galles'),
    )

    palyer_id       = models.ForeignKey(User)
    tournament_id   = models.ForeigneKey(Tournament)
    first_team      = models.CharField(max_length=15, choices=teams, default='--')
    second_team     = models.CharField(max_length=15, choices=teams, default='--')
    third_team      = models.CharField(max_length=15, choices=teams, default='--')
    fourth_team     = models.CharField(max_length=15, choices=teams, default='--')
    fifth_team      = models.CharField(max_length=15, choices=teams, default='--')
    sixth_team      = models.CharField(max_length=15, choices=teams, default='--')
    grand_slam      = models.BooleanField(default=False)
    wooden_spoon    = models.BooleanField(default=False)
    points_won      = models.IntegerField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now_add=True)

class BetPoint(models.Model): 
    """
    BetPoint model is a key/value table that store 
    - each element of bet as key
    - each point of winning element as value
    """
    key             = models.CharField()
    value           = models.IntegerField()
