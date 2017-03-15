from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

import logging
clog = logging.getLogger("django")
clog.setLevel( logging.ERROR )
clog.addHandler( logging.StreamHandler() )
clog.debug('This is tournaments/models')

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

class TeamStat(models.Model):
    team        = models.ForeignKey(Team)
    tournament  = models.ForeignKey(Tournament)
    played      = models.IntegerField(null=True, blank=True, default=0)
    win         = models.IntegerField(null=True, blank=True, default=0)
    draw        = models.IntegerField(null=True, blank=True, default=0)
    lose        = models.IntegerField(null=True, blank=True, default=0)
    ptsfor      = models.IntegerField(null=True, blank=True, default=0)
    ptsagainst  = models.IntegerField(null=True, blank=True, default=0)
    ptsdiff     = models.IntegerField(null=True, blank=True, default=0)
    tryfor      = models.IntegerField(null=True, blank=True, default=0)
    tryagainst  = models.IntegerField(null=True, blank=True, default=0)
    trybonus    = models.IntegerField(null=True, blank=True, default=0)
    losebonus   = models.IntegerField(null=True, blank=True, default=0)
    points      = models.IntegerField(null=True, blank=True, default=0)

    def __unicode__(self):
        return "%s : %s" % (
            self.tournament,
            self.team
        )

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
    tournament      = models.ForeignKey( Tournament )
    date            = models.DateTimeField( auto_now_add=False )
    cup_round       = models.CharField(max_length=1, choices=cup_round, default='1')
    #tournament_round = models.IntegerField()
    home_team       = models.ForeignKey(Team, related_name="home_team" )
    home_team_score = models.IntegerField( null=True, blank=True )
    home_team_tries = models.IntegerField( null=True, blank=True )
    home_team_bonus = models.CharField( max_length=15, choices=bonus, default='--' )
    home_team_point = models.IntegerField( null=True, blank=True )
    away_team       = models.ForeignKey( Team, related_name="away_team" )
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
        return "%s vs %s" % (self.home_team, self.away_team)

class TeamMatchPoint(models.Model):
    """
    Team model
    """
    team        = models.ForeignKey(Team)
    match       = models.ForeignKey(Match)
    victory     = models.IntegerField(null=True, blank=True, default=0)
    draw        = models.IntegerField(null=True, blank=True, default=0)
    trybonus    = models.IntegerField(null=True, blank=True, default=0)
    losebonus   = models.IntegerField(null=True, blank=True, default=0)
    points      = models.IntegerField(null=True, blank=True, default=0)

    def __unicode__(self):
        return "Round %s - %s vs %s => %s" % (
            self.match.cup_round,
            self.match.home_team,
            self.match.away_team,
            self.team
        )

@receiver(post_save, sender=Match)
def update_team_points(sender, instance, **kwargs):
    """
    each time, there is a modification on a match, team_score will be updated
    """
    clog.debug("update_team_points")
    home_points = 0
    away_points = 0
    gap = instance.home_team_score - instance.away_team_score

    #home_team_points = TeamMatchPoint(match = instance, team = instance.home_team)
    #away_team_points = TeamMatchPoint(match = instance, team = instance.away_team)

    away_team_points    = TeamMatchPoint.objects.filter(match = instance).filter(team = instance.away_team)
    home_team_points    = TeamMatchPoint.objects.filter(match = instance).filter(team = instance.home_team)
    clog.debug(" len(away_team_points) = " + str(len(away_team_points)))
    clog.debug(" len(home_team_points) = " + str(len(home_team_points)))
    # check if object teampoints exists
    if len(away_team_points) == 0:
        away_team_points = TeamMatchPoint(team = instance.away_team, match = instance)
        clog.debug("create away TeamPoint " + str(dir(away_team_points)))
    else:
        away_team_points = TeamMatchPoint.objects.get(match = instance, team = instance.away_team)
        clog.debug("update away TeamPoint " + str(dir(away_team_points)))
    if len(home_team_points) == 0:
        clog.debug("create home TeamPoints " + str(dir(home_team_points)))
        home_team_points = TeamMatchPoint(team = instance.home_team, match = instance)
    else:
        clog.debug("update away TeamPoint " + str(dir(home_team_points)))
        home_team_points = TeamMatchPoint.objects.get(team = instance.home_team, match = instance)

    # victory : +4
    # tries >= 4 : +1
    # TODO if team has 5 vitories : +3
    #
    # defeat : +0
    # score <= 7 : +1
    # tries >= 4 : +1


    # Victory - Defeat
    if instance.home_team_score > instance.away_team_score:
        home_team_points.victory = 4
        away_team_points.victory = 0
    if instance.home_team_score < instance.away_team_score:
        home_team_points.victory = 0
        away_team_points.victory = 4

    # Draw
    if instance.home_team_score == instance.away_team_score:
        home_team_points.victory = 2
        away_team_points.victory = 2

    home_points += home_team_points.victory
    away_points += away_team_points.victory


    # try bonus
    if instance.home_team_tries >= 4:
        home_team_points.trybonus = 1
    if instance.away_team_tries >= 4:
        away_team_points.trybonus = 1

    home_points += home_team_points.trybonus
    away_points += away_team_points.trybonus

    # lose bonus
    if abs(gap) <= 7:
        if instance.home_team_score < instance.away_team_score:
            home_team_points.losebonus = 1
        if instance.away_team_score < instance.home_team_score:
            away_team_points.losebonus = 1

    home_points += home_team_points.losebonus
    away_points += away_team_points.losebonus

    home_team_points.points = home_points
    clog.debug("save points home_team")
    home_team_points.save()
    away_team_points.points = away_points
    clog.debug("save points away_team")
    away_team_points.save()

@receiver(post_save, sender=TeamMatchPoint)
def update_team_stats(sender, instance, **kwargs):
    """
    each end of match, recompute stats of teams
    It's better than to update at each teammatchpoints update
    """
    clog.debug("update_team_stats")
    home_team       = instance.match.home_team
    away_team       = instance.match.away_team
    clog.debug("home_team = " + str(home_team))
    clog.debug("away_team = " + str(away_team))
    clog.debug("------------------------- get object home_team_match ------------------------------------------")
    home_team_match = Match.objects.filter(models.Q(home_team = home_team) | models.Q(away_team = home_team)).filter(date__gte = instance.match.tournament.begins)
    clog.debug("------------------------- get object away_team_match ------------------------------------------")
    away_team_match = Match.objects.filter(models.Q(home_team = away_team) | models.Q(away_team = away_team)).filter(date__gte = instance.match.tournament.begins)

    try:
        home_stats      = TeamStat.objects.get(team = home_team, tournament = instance.match.tournament)
    except Exception, e:
        clog.debug(e)
        home_stats      = TeamStat(team = home_team, tournament = instance.match.tournament)
    try:
        away_stats      = TeamStat.objects.get(team = away_team, tournament = instance.match.tournament)
    except Exception, e:
        clog.debug(e)
        away_stats      = TeamStat(team = away_team, tournament = instance.match.tournament)


    # TODO convert the folowing into a function
    played      = 0
    win         = 0
    draw        = 0
    lose        = 0
    ptsfor      = 0
    ptsagainst  = 0
    ptsdiff     = 0
    tryfor      = 0
    tryagainst  = 0
    trybonus    = 0
    losebonus   = 0
    points      = 0

    for m in home_team_match:
        played += 1
        if home_team == m.home_team:
            clog.debug("stat for home_team => " + str(m.home_team.name))
            if m.home_team_score > m.away_team_score:
                win += 1
            if m.home_team_score == m.away_team_score:
                draw += 1
            if m.home_team_score < m.away_team_score:
                lose += 1
                if m.away_team_score - m.home_team_score <= 7:
                    losebonus += 1
            if m.home_team_tries >= 4:
                trybonus += 1
            clog.debug("home_team is " + str(m.home_team) + "ptsfor => " + str(m.home_team_score) + "ptsagainst => " + str(m.away_team_score))
            ptsfor      += m.home_team_score
            ptsagainst  += m.away_team_score
            tryfor      += m.home_team_tries
            tryagainst  += m.away_team_tries

        else:
            clog.debug("stat for home_team => " + str(m.away_team.name))
            if m.away_team_score > m.home_team_score:
                win += 1
            if m.away_team_score == m.home_team_score:
                draw += 1
            if m.away_team_score < m.home_team_score:
                lose += 1
                if m.home_team_score - m.away_team_score <= 7:
                    losebonus += 1
            if m.away_team_tries >= 4:
                trybonus += 1
            clog.debug("away_team is " + str(m.away_team) + "ptsfor => " + str(m.away_team_score) + "ptsagainst => " + str(m.home_team_score))
            ptsfor      += m.away_team_score
            ptsagainst  += m.home_team_score
            tryfor      += m.away_team_tries
            tryagainst  += m.home_team_tries

        clog.debug("Equipe: " + str(home_stats.team))
        clog.debug("played: " + str(played))
        clog.debug("win: " + str(win))
        clog.debug("draw: " + str(draw))
        clog.debug("lose: " + str(lose))
        clog.debug("trybonus: " + str(trybonus))
        clog.debug("losebonus: " + str(losebonus))
        clog.debug("ptsfor: " + str(ptsfor))
        clog.debug("ptsagainst: " + str(ptsagainst))
        clog.debug("tryfor: " + str(tryfor))
        clog.debug("tryagainst: " + str(tryagainst))

    home_stats.played       = played
    home_stats.win          = win
    home_stats.draw         = draw
    home_stats.lose         = lose
    home_stats.ptsfor       = ptsfor
    home_stats.ptsagainst   = ptsagainst
    home_stats.tryfor       = tryfor
    home_stats.tryagainst   = tryagainst
    home_stats.trybonus     = trybonus
    home_stats.losebonus    = losebonus
    home_stats.ptsdiff      = ptsfor - ptsagainst
    home_stats.points       = win * 4 + draw * 2 + trybonus + losebonus
    # compute grand slam
    home_stats.points       += 3 if win == 5 else 0

    played      = 0
    win         = 0
    draw        = 0
    lose        = 0
    ptsfor      = 0
    ptsagainst  = 0
    ptsdiff     = 0
    tryfor      = 0
    tryagainst  = 0
    trybonus    = 0
    losebonus   = 0
    points      = 0

    for m in away_team_match :
        played += 1
        if away_team == m.home_team:
            if m.home_team_score > m.away_team_score:
                win += 1
            if m.home_team_score == m.away_team_score:
                draw += 1
            if m.home_team_score < m.away_team_score:
                lose += 1
                if m.away_team_score - m.home_team_score <= 7:
                    losebonus += 1
            if m.home_team_tries >= 4:
                trybonus += 1

            ptsfor      += m.home_team_score
            ptsagainst  += m.away_team_score
            tryfor      += m.home_team_tries
            tryagainst  += m.away_team_tries

        else:
            if m.away_team_score > m.home_team_score:
                win += 1
            if m.away_team_score == m.home_team_score:
                draw += 1
            if m.away_team_score < m.home_team_score:
                lose += 1
                if m.home_team_score - m.away_team_score <= 7:
                    losebonus += 1
            if m.away_team_tries >= 4:
                trybonus += 1
            ptsfor      += m.away_team_score
            ptsagainst  += m.home_team_score
            tryfor      += m.away_team_tries
            tryagainst  += m.home_team_tries

        clog.debug("Equipe: " + str(away_stats.team))
        clog.debug("played: " + str(played))
        clog.debug("win: " + str(win))
        clog.debug("draw: " + str(draw))
        clog.debug("lose: " + str(lose))
        clog.debug("trybonus: " + str(trybonus))
        clog.debug("losebonus: " + str(losebonus))
        clog.debug("ptsfor: " + str(ptsfor))
        clog.debug("ptsagainst: " + str(ptsagainst))
        clog.debug("tryfor: " + str(tryfor))
        clog.debug("tryagainst: " + str(tryagainst))


    away_stats.played       = played
    away_stats.win          = win
    away_stats.draw         = draw
    away_stats.lose         = lose
    away_stats.ptsfor       = ptsfor
    away_stats.ptsagainst   = ptsagainst
    away_stats.tryfor       = tryfor
    away_stats.tryagainst   = tryagainst
    away_stats.trybonus     = trybonus
    away_stats.losebonus    = losebonus
    away_stats.ptsdiff      = ptsfor - ptsagainst
    away_stats.points       = win * 4 + draw * 2 + trybonus + losebonus
    # compute grand slam
    away_stats.points       += 3 if win == 5 else 0

    clog.debug("save stats home_team")    
    home_stats.save()
    clog.debug("save stats away_team")
    away_stats.save()


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
