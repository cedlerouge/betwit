from __future__ import unicode_literals
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from tournaments.models import Match, Tournament, Team
import math
import pytz

import logging                              
logger = logging.getLogger("django")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
logger.info('This is info bets/models')
logger.debug("This is debug bets/models")


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
    try:
        instance.profile.save()
    except :
        Profile.objects.create(user = instance)


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
    points_won      = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return str(self.player) + " - " + str(self.match)

class BetPoint(models.Model):
    """
    This is to store 
    * points
    * bet id
    * date 
    * player id 
    without create too much matchrating entries at the end of match (because of updaterating function)
    """
    player      = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    match       = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    matchbet    = models.ForeignKey(MatchBet, on_delete=models.DO_NOTHING)
    points_won  = models.FloatField(default=0.0)
    def __unicode__(self):
        return "player %s - %s vs %s => %s" % (
            self.player,
            self.match.home_team,
            self.match.away_team,
            self.points_won
        )


class MatchRating(models.Model):
    """
    Rating model : three rates by match
        * one rate for the home team : ht_rating
        * one rate for the away team : at_rating
        * one rate for the null match : null_rating
    """
    match           = models.ForeignKey(Match)
    ht_votes        = models.IntegerField(default=0)
    at_votes        = models.IntegerField(default=0)
    null_votes      = models.IntegerField(default=0)
    total_votes     = models.IntegerField(default=0)
    ht_rating       = models.FloatField(default=0)
    at_rating       = models.FloatField(default=0)
    null_rating     = models.FloatField(default=0)
    date            = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=MatchBet)
def update_rating(sender, instance, **kwargs):
    """
    base = 4
    rating = MAX(LOG(bets_total/bets_on_team;base)*10;1)
    1- recuperer l'id du match
    2- recuperer tous les paris sur ce match
    3- compter le nombre de vote pour chaque equipe
    4- calculer la cote
    5- mettre a jour la cote du match
    """
    base = 5
    #logger.info()
    match = Match.objects.get( id = instance.match.id)
    match_bets   = MatchBet.objects.filter(match = match)
    ht_votes = 0
    at_votes = 0
    null_votes = 0
    for b in match_bets:
        if b.home_team_score > b.away_team_score:
            ht_votes += 1
        elif b.home_team_score < b.away_team_score:
            at_votes += 1
        else :
            null_votes += 1
    total_votes = ht_votes + at_votes + null_votes
    ht_rating = max(math.log(float(total_votes)/float((ht_votes if  ht_votes != 0 else 1)),base)*10,1)
    at_rating = max(math.log(float(total_votes)/float((at_votes if  at_votes != 0 else 1)),base)*10,1)
    null_rating = max(math.log(float(total_votes)/float((null_votes if  null_votes != 0 else 1)) ,base)*10,1)

    rate = MatchRating()
    rate.match = match
    rate.ht_votes = ht_votes
    rate.at_votes = at_votes
    rate.null_votes = null_votes
    rate.ht_rating = round(ht_rating,2)
    rate.at_rating = round(at_rating,2)
    rate.null_rating = round(null_rating,2)
    rate.total_votes = total_votes
    rate.save()

    # TODO creer un table ratings(id , id_match, ht_rating, at_rating, null_rating)
    # TODO ajouter une cote par paris ou creer une base time serie pour stocker l'evolution de la cote pour un match
    # TODO creer une base time serie pour stocker l'evolution du classement de chaque joueur


@receiver(post_save, sender=Match)
def update_matchbet_points(sender, instance, **kwargs):
    # The rate of a match must be set
    last_rate = MatchRating.objects.filter(match = instance).order_by('-date').first()
    rate = 0
    logger.debug('-----------last_rate---------------' + str(last_rate))
    if last_rate is not None :
        if instance.home_team_score > instance.away_team_score:
            rate = last_rate.ht_rating
        elif instance.home_team_score < instance.away_team_score:
            rate = last_rate.at_rating
        else :
            rate = last_rate.null_rating
    
        match_bets   = MatchBet.objects.filter(match = instance)
        for b in match_bets:
            logger.debug('-----user ------: ' + str(b.player))
            points  = 0
            logger.info('points => ' + str(points))
            # compute Victory
            logger.info('--Victory--')
            if b.home_team_score > b.away_team_score and instance.home_team_score > instance.away_team_score:
                points += 2 * rate
            elif b.home_team_score < b.away_team_score and instance.home_team_score < instance.away_team_score:
                points += 2 * rate
            elif b.home_team_score == b.away_team_score and instance.home_team_score == instance.away_team_score:
                points += 2 * rate
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

            
            # compute the good score
            if b.home_team_score == instance.home_team_score and b.away_team_score == instance.away_team_score:
                logger.info('--goodscore--')
                points += 6
            else :
                # compute gap
                logger.info('--gap--')
                #b_gap = b.home_team_score - b.away_team_score if b.home_team_score > b.away_team_score else b.away_team_score - b.home_team_score
                #m_gap = instance.home_team_score - instance.away_team_score if instance.home_team_score > instance.away_team_score else instance.away_team_score - instance.home_team_score
                b_gap = b.home_team_score - b.away_team_score
                m_gap = instance.home_team_score - instance.away_team_score
                if b_gap == m_gap:
                    points += 2
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
            if 'Null'.lower() in  b.home_team_bonus.lower():
                points +=0
            elif b.home_team_bonus.lower() in instance.home_team_bonus.lower():
                points += 1
            else:
                points -= 1
            logger.info('b.home_team_bonus => ' + str(b.home_team_bonus))
            logger.info('instance.home_team_bonus => ' + str(instance.home_team_bonus))
            logger.info('points => ' + str(points))

            # compute away_team_bonus
            logger.info('--away bonus--')
            if 'Null'.lower() in  b.away_team_bonus.lower():
                points +=0
            elif b.away_team_bonus.lower() in instance.away_team_bonus.lower():
                points += 1
            else:
                points -= 1
            logger.info('points => ' + str(points))

            # Create or update betpoint emtry
            bet_points = BetPoint.objects.filter(matchbet = b)
            if not bet_points:
                bpoints = BetPoint()
                bpoints.match = b.match
                bpoints.matchbet = b
                bpoints.player = b.player
            else:
                bpoints = bet_points[0]
            
            bpoints.points_won = points
            logger.info("b.points_won ==============> " + str(bpoints.points_won))
            bpoints.save()







class TournamentBet(models.Model):
    """
    Tournament Bets model : one bet per player
    """
    player          = models.ForeignKey(User)
    tournament      = models.ForeignKey(Tournament)
    first_team      = models.ForeignKey(Team, related_name='first_team')
    second_team     = models.ForeignKey(Team, related_name='second_team')
    third_team      = models.ForeignKey(Team, related_name='third_team')
    fourth_team     = models.ForeignKey(Team, related_name='fourth_team')
    fifth_team      = models.ForeignKey(Team, related_name='fifth_team')
    sixth_team      = models.ForeignKey(Team, related_name='sixth_team')
    grand_slam      = models.BooleanField(default=False)
    wooden_spoon    = models.BooleanField(default=False)
    points_won      = models.IntegerField(null=True, blank=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now_add=True)