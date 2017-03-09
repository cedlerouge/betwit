from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Match, Tournament
import pytz



# Create your models here.

class Profile(models.Model):
    user            = models.OneToOneField( User, on_delete=models.CASCADE)
    is_admin        = models.BooleanField(default=False)
    tz              = models.CharField(max_length=30,default='Europe/Paris')
    points_won      = models.IntegerField( null=True, default=0 )


@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user = instance)

@receiver(post_save, sender=User)
def update_profile(sender, instance, **kwargs):
    instance.profile.save()

class MatchBet(models.Model):
    bonus_choices   = (
        ( 'Null', 'Null'), 
        ('Defense', 'Defense'),
        ('Attack', 'Attack' ),
    )
    """
    Bets model : one bet per match and per player
    """
    player_id       = models.ForeignKey(User)
    match_id        = models.ForeignKey(Match)
    home_team_score = models.IntegerField()
    home_team_tries = models.IntegerField()
    home_team_bonus = models.CharField(max_length=15, choices=bonus_choices, default='--')
    away_team_score = models.IntegerField()
    away_team_tries = models.IntegerField()
    away_team_bonus = models.CharField(max_length=15, choices=bonus_choices, default='--')
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
    # DONE in TournamentBetForm
    #matchs = Match.objects.filter( tournament_id = tid )
    #teams = list()
    #for m in matchs: 
    #    t = (m.home_team_id.name, m.home_team_id.name)
    #    if t not in teams:
    #        team.append(t)
    #teams = (
    #  ('an', 'Angleterre'),
    #  ('ec', 'Ecosse'),
    #  ('fr', 'France'),
    #  ('ir', 'Irlande'),
    #  ('it', 'Italie'),
    #  ('pg', 'Pays de Galles'),
    #)

    player_id       = models.ForeignKey(User)
    tournament_id   = models.ForeignKey(Tournament)
    #first_team      = models.CharField(max_length=15, choices=teams, default='--')
    #second_team     = models.CharField(max_length=15, choices=teams, default='--')
    #third_team      = models.CharField(max_length=15, choices=teams, default='--')
    #fourth_team     = models.CharField(max_length=15, choices=teams, default='--')
    #fifth_team      = models.CharField(max_length=15, choices=teams, default='--')
    #sixth_team      = models.CharField(max_length=15, choices=teams, default='--')
    first_team      = models.CharField(max_length=15)
    second_team     = models.CharField(max_length=15)
    third_team      = models.CharField(max_length=15)
    fourth_team     = models.CharField(max_length=15)
    fifth_team      = models.CharField(max_length=15)
    sixth_team      = models.CharField(max_length=15)
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
    key             = models.CharField(max_length=200)
    value           = models.IntegerField()
