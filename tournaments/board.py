from .models import Tournament, Match, Team, MatchPoint, TeamMatchPoint, TeamStat
from django.utils import timezone

def getTeamList(tournament_id):
    matchs          = Match.objects.filter( tournament = tournament_id ).order_by( "round" ).order_by('date')
    team_list       = []
    for m in matchs:
        if m.home_team not in team_list:
            team_list.append(m.home_team)
    return team_list

def getTeamTable(tournament_id):
    team_stat = TeamStat.objects.filter(tournament = tournament_id)
    results_list = []
    try:
        for ts in team_stat:
            results_list.append(ts)
        results_list.sort(key = attrgetter('points','ptsdiff'), reverse=True)
    except:
        pass
    return results_list

def getNextMatchs(tournament_id, limit):
    matchs     = Match.objects.filter( tournament = tournament_id, date__gte = timezone.now( )).order_by( "round" ).order_by('date')[:limit]
    match_list = []
    for m in matchs:
        match_list.append(m)
    return match_list