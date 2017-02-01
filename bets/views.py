from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils import timezone
import datetime

from .models import MatchBet, TournamentBet
from .forms import MatchBetForm, TournamentBetForm, BetPointForm

# Create your views here.

class Index(View):
    def get(self, request):
        #return HttpResponse('I am called from a get Request')
        return render(request, 'base.html')
    def post(self, request):
        #return HttpResponse('I am called from a post Request')
        return render(request, 'base.html')

class UserRedirect(View):
    def get(self, request):
        if request.user.is_authenticated():
            # TODO mettre en place des logs
            #logger.info('authorized user')
            return HttpResponseRedirect(request.user.username)
        else:
            #logger.info('unauthorized user')
            return HttpResponseRedirect('/accounts/login/')


class Profile(View):
    """
    User home reachable from /user/<username>/ URL
    """
    #@login_required
    def get(self, request, username=None):
        if not username:
            username = request.user.username
        # limit private page to only the user
        # if request.user.username == username
        params      = dict()
        userProfile = User.objects.get(username=request.user.username)
        matchBet    = MatchBet.objects.filter(player_id=userProfile)
        tournamentBet   = TournamentBet.objects.filter(player_id=userProfile)
    #    for obj in betcup:
    #        obj.fields = dict((field.name, field.value_to_string(obj))
    #                                            for field in obj._meta.fields)
    #    form       = BetForm()
        params['bets'] = matchBet
        params['user'] = userProfile
        params['betcup'] = tournamentBet
        return render(request, 'bets/profile.html', params)


def bet_list( request ):
    bet_list    = Bet.objects.order_by( '-year' )
    context     = { 'bet_list':bet_list }
    return render( request, 'bets/bet_list.html', context )




#class BetView( View )
