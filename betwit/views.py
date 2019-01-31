from __future__ import unicode_literals

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View

from django.contrib.auth.models import User

from bets.models import MatchBet, TournamentBet
from tournaments.models import Tournament, Match
from andablog.models import Entry
import tournaments.board
from operator import itemgetter
import datetime
from django.db.models import Q

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
            tournament_bets   = TournamentBet.objects.filter(player = user).last()
            score     = sum(int(b['points_won'] if b['points_won'] is not None else 0 ) for b in match_bets.values())
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
                if best_score <= int(b['points_won'] if b['points_won'] is not None else 0):
                    best_score = int(b['points_won'] if b['points_won'] is not None else 0)
            first5.append( (user.username, score, best_score) )
        first5.sort(key = itemgetter(1, 2), reverse = True)
        return first5[:5]

    def get(self, request):
        limit = 1
        tid = Tournament.objects.filter(state=1,year=datetime.datetime.now().year)
        next_match = Match.objects.filter(tournament = tid).order_by('date')[0]
        content = {

            # Blog
            'entries':  Entry.objects.filter(Q(is_published=True) | Q(author__isnull=False)).order_by('-published_timestamp'),
            #comments = Comment.objects.last(5)

            # CountDown
            'cntdn': next_match,
            'cntdn_tgd': next_match.date,
            # player rank 
            'first5': self.first_players(),
            # tournament
            'team_stats': tournaments.board.getTeamTable(tid)

        }

        return render(request, self.template_name, { 'content': content })
