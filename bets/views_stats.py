from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from .models import MatchBet, TournamentBet, BetPoint, MatchRating

import json



@login_required
def stats(request):
    params = {'error_message': None, 'bp_series': list() }
    users = User.objects.all()
    bp_series = []
    for user in users:
        match_bets  = MatchBet.objects.filter(player = user)
        bp          = BetPoint.objects.filter(player = user)
        serie       = {
            'name': str(user.username),
            'data': [['start',0]]
        }
        sum_pts = 0
        for p in bp:
            sum_pts += p.points_won
            serie['data'].append([p.match.str(),sum_pts])
        bp_series.append(serie)
    params['bp_series'] = json.dumps(bp_series)
    return render(request, 'bets/stats.html', {'content': params})

@login_required
def stats_perso(request, username=None):
    if not username:
        username = request.user.username
    params = {'error_message': None, 'bp_series': list() }
    user = User.objects.get(username = username)
    bp_series = []
    match_bets  = MatchBet.objects.filter(player = user)
    bp          = BetPoint.objects.filter(player = user)
    xcategories = []
    serie       = {
        'name': 'Points',
        'data': []
    }
    for p in bp:
        xcategories.append(p.match.str())
        serie['data'].append(p.points_won)
    params['serie'] = json.dumps(serie)
    params['categories'] = json.dumps(xcategories)
    return render(request, 'bets/stats_perso.html', {'content': params})


#@login_required
#def stats_perso(request, username=None):
#    if not username:
#        username = request.user.username
#    params = {'error_message': None, 'bp_series': list() }
#    per_round_series = []
#    rounds = []
#
#    match_bets  = MatchBet.objects.filter(player = user)
#    bp          = BetPoint.objects.filter(player = user)
#    for b in bp:
#        if b.match.cup_round not in rounds:
#            rounds.append(b.match.cup_round)
#        
#    serie       = {
#            'name': str(user.username),
#            'data': [['start',0]]
#        }
#    sum_pts = 0
#    for p in bp:
#        sum_pts += p.points_won
#        serie['data'].append([p.match.str(),sum_pts])
#    bp_series.append(serie)
#    params['bp_series'] = json.dumps(bp_series)
#    return render(request, 'bets/stats.html', {'content': params})