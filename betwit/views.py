from __future__ import unicode_literals

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Sum

from django.contrib.auth.models import User

from bets.models import MatchBet, TournamentBet, MatchRating, BetPoint
from tournaments.models import Tournament, Match
from andablog.models import Entry
import tournaments.board
from operator import itemgetter
import datetime
from django.db.models import Q


import logging
logger = logging.getLogger('django')
logger.info('This is betwit/views')


class Index(View):
    def get(self, request):
        #return HttpResponse('I am called from a get Request')
        return render(request, 'base.html')
    def post(self, request):
        #return HttpResponse('I am called from a post Request')
        return render(request, 'base.html')

class Rules(View):
    def get(self, request):
        return render(request, 'rules.html')

class Cote(View):
    def get(self, request):
        return render(request, 'cote.html')

class Apropos(View):
    def get(self, request):
        return render(request, 'apropos.html')

class Players(View):
    def get(self, request):
        if request.user.is_authenticated(): 
            return render(request, 'slides.html')
        else:
            return HttpResponseRedirect('/accounts/login/')

class HomeView(View):
    template_name = 'home.html'

    def first_players(self):
        users = User.objects.all()
        first5 = list()

        for user in users:
            
            match_bets        = MatchBet.objects.filter(player = user)
            #tournament_bets   = TournamentBet.objects.filter(player = user).last()
            score     = sum(float(b['points_won'] if b['points_won'] is not None else 0 ) for b in match_bets.values())
            # I don't use tournament_bet for simplicity
            #try:
            #    # if tournament_bets != Null
            #    scoref    = score + tournament_bets.points_won
            #except:
            #    scoref    = score
            #first5.append((user.username, scoref))
            # find best score per prognosis
            best_score = 0
            for b in match_bets.values():
                if best_score <= float(b['points_won'] if b['points_won'] is not None else 0):
                    best_score = float(b['points_won'] if b['points_won'] is not None else 0)
            first5.append( (user.username, score, best_score) )
        first5.sort(key = itemgetter(1, 2), reverse = True)
        first5 = BetPoint.objects.values('player').annotate(Sum('points_won')).order_by('-points_won__sum')[:5]
        # retrieve username
        for b in first5:
            b['player'] = User.objects.get(id = b['player'])
        return first5

    def get(self, request):
        limit = 1
        tid = Tournament.objects.filter(state=1,year=datetime.datetime.now().year)
        #next_match = Match.objects.filter(tournament = tid).order_by('date')[0]
        next_matchs = tournaments.board.getNextMatchs(tid,3)
        # rassemble match informations and ratings in a table
        matchs = list()
        for m in next_matchs:
            i = dict()
            try:
                rating = MatchRating.objects.filter( match = m).order_by("-date")[0]
                i['ht_rating'] = rating.ht_rating
                i['at_rating'] = rating.at_rating
                i['null_rating'] = rating.null_rating
            except:
                i['ht_rating'] = 1
                i['at_rating'] = 1
                i['null_rating'] = 1
            i['date'] = m.date
            i['ht'] = m.home_team
            i['at'] = m.away_team
            matchs.append(i)
        content = {

            # Blog
            'entries':  Entry.objects.filter(Q(is_published=True) | Q(author__isnull=False)).order_by('-published_timestamp'),
            #comments = Comment.objects.last(5)

            # CountDown
            # At the end of the tournament, display NaN when there is no more match
            'cntdn': matchs[0] if len(matchs)>0 else None ,
            'cntdn_tgd': matchs[0]['date'] if len(matchs)>0 else None,
            'next_matchs': matchs if len(matchs)>0 else None,
            # player rank 
            'first5': self.first_players(),
            # tournament
            'team_stats': tournaments.board.getTeamTable(tid)

        }

        return render(request, self.template_name, { 'content': content })
