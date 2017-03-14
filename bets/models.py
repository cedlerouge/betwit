from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Match, Tournament
import pytz

import logging
logger = logging.getLogger('django')
logger.setLevel( logging.DEBUG )
logger.addHandler( logging.StreamHandler() )
logger.info('This is bets/models')


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
    player          = models.ForeignKey(User)
    match           = models.ForeignKey(Match)
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

@receiver(post_save, sender=Match)
def update_matchbet_points(sender, instance, **kwargs):
    # The odds of a match must be set
    if instance.odds > 0 :
        match_bets   = MatchBet.objects.filter(match = instance)
        for b in match_bets:
            logger.info('-----user ------: ' + str(b.player))
            points  = 0
            logger.info('points => ' + str(points))
            # compute Victory
            logger.info('--Victory--')
            if b.home_team_score > b.away_team_score and instance.home_team_score > instance.away_team_score:
                points += 2 * instance.odds
            elif b.home_team_score < b.away_team_score and instance.home_team_score < instance.away_team_score:
                points += 2 * instance.odds
            elif b.home_team_score == b.away_team_score and instance.home_team_score == instance.away_team_score:
                points += 2 * instance.odds
            logger.info('points => ' + str(points))

            # compute score
            logger.info('--score--')
            if b.home_team_score == instance.home_team_score:
                points += 1
            if b.away_team_score == instance.away_team_score:
                points += 1
            logger.info('points => ' + str(points))

            # compute try
            logger.info('--try--')
            if b.home_team_tries == instance.home_team_tries:
                points += 1
            if b.away_team_tries == instance.away_team_tries:
                points += 1
            logger.info('points => ' + str(points))

            # compute gap
            logger.info('--gap--')
            #b_gap = b.home_team_score - b.away_team_score if b.home_team_score > b.away_team_score else b.away_team_score - b.home_team_score
            #m_gap = instance.home_team_score - instance.away_team_score if instance.home_team_score > instance.away_team_score else instance.away_team_score - instance.home_team_score
            b_gap = b.home_team_score - b.away_team_score
            m_gap = instance.home_team_score - instance.away_team_score
            if b_gap == m_gap:
                points += 2
            logger.info('points => ' + str(points))

            # compute the good score
            logger.info('--goodscore--')
            if b.home_team_score == instance.home_team_score and b.away_team_score == instance.away_team_score:
                points += 6
            logger.info('points => ' + str(points))

            # compute card
            logger.info('--card--')
            logger.info('b.card: ' + str(b.card))
            logger.info('instance.card: ' + str(instance.card))
            if b.card and instance.card :
                points += 1
            elif b.card and not instance.card:
                points -= 1
            logger.info('points => ' + str(points))

            # compute drop
            logger.info('--dropgoal--')
            logger.info('b.drop_goal' + str(b.drop_goal))
            logger.info('m.drop_goal' + str(instance.drop_goal))
            if b.drop_goal and instance.drop_goal :
                points += 1
            elif b.drop_goal and not instance.drop_goal:
                points -= 1
            logger.info('points => ' + str(points))

            # compute fight
            logger.info('--fight--')
            if b.fight and instance.fight :
                points += 2
            elif b.fight and not instance.fight:
                points -= 2
            logger.info('points => ' + str(points))

            # compute home_team_bonus
            logger.info('--home bonus--')
            if 'Null'.lower() ==  b.home_team_bonus.lower():
                points +=0
            elif b.home_team_bonus.lower() == instance.home_team_bonus.lower():
                points += 1
            else:
                points -= 1
            logger.info('points => ' + str(points))

            # compute away_team_bonus
            logger.info('--away bonus--')
            if 'Null'.lower() ==  b.away_team_bonus.lower():
                points +=0
            elif b.away_team_bonus.lower() == instance.away_team_bonus.lower():
                points += 1
            else:
                points -= 1
            logger.info('points => ' + str(points))

            b.points_won = points
            b.save()







class TournamentBet(models.Model):
    """
    Tournament Bets model : one bet per player
    """

    # TODO rendre cette list dynamique
    # DONE in TournamentBetForm
    #matchs = Match.objects.filter( tournament = tid )
    #teams = list()
    #for m in matchs:
    #    t = (m.home_team.name, m.home_team.name)
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

    player          = models.ForeignKey(User)
    tournament      = models.ForeignKey(Tournament)
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
