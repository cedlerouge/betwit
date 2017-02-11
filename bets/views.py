from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.http import require_http_methods

from django.utils import timezone
import datetime

from tournaments.models import Tournament, Match
from .models import MatchBet, TournamentBet
from .forms import MatchBetForm, TournamentBetForm, BetPointForm

import logging
logger = logging.getLogger('django')
logger.setLevel( logging.DEBUG )
logger.addHandler( logging.StreamHandler() )
logger.info('This is it')

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
    Display a page with every bets of the last tournament (last to the first)
    """
    #@login_required
    def get(self, request, username=None):
        if not username:
            username = request.user.username
        # limit private page to only the user
        # if request.user.username == username
        params      = dict()
        userProfile = User.objects.get(username=request.user.username)
        tournament  = Tournament.objects.filter(year=datetime.datetime.now().year)
        last_tournament_with_bet = None
        lm          = list()
        for t in tournament:
            last_tournament_with_bet = t
            logger.debug( "tournament => " + t.name )
            tournamentBet   = None
            tbetForm        = None
            tournamentBet   = TournamentBet.objects.filter( tournament_id=t ).filter( player_id = userProfile ).first()
            if tournamentBet:
                tbetForm    = TournamentBetForm( instance=tournamentBet )
                match       = Match.objects.filter( tournament_id=t )
                for m in match :
                    matchBet = None
                    matchBet    = MatchBet.objects.filter( match_id = m ).filter( player_id = userProfile ).first()
                    if matchBet:
                        lm.append(matchBet)
 
        #        break
    #    for obj in betcup:
    #        obj.fields = dict((field.name, field.value_to_string(obj))
    #                                            for field in obj._meta.fields)
    #    form       = BetForm()
        params['mbet'] = lm
        params['user'] = userProfile
        params['tbet'] = tbetForm
        params['tournament'] = last_tournament_with_bet
        if last_tournament_with_bet.begins > timezone.now() and tournamentBet is not None:
            params['betcup_is_update'] = True
            params['betcup_update_url'] = reverse( 'bets:tbet_add', args=(last_tournament_with_bet.id, tournamentBet.id))
        params['current_date'] = timezone.now()
        return render(request, 'bets/profile.html', params)

@require_http_methods(["GET", "POST"])
def matchBet_add( request, tournament_id=None, mbet_id=None, m_id=None ):
    logger.info("matchbet")
    params          = {'error_message': None, 'is_update': None }
    if request.method == 'POST':
        user        = User.objects.get(username=request.user.username)
        form        = MatchBetForm(request.POST)
        logger.info (" je suis le formulaire poste de matchbet_add: ", str(form.fields))
        if form.is_valid():
            if mbet_id is not None:
                # TODO Do not let save a match bet if an user has already his one for a specified match id
                mbet                = get_object_or_404(MatchBet, pk=mbet_id)
                logger.info('mbet_id is present, so this is update')
                logger.info('mbet.id:' + str(mbet.id))  
                logger.info('mbet.home_team_score:' + str(mbet.home_team_score))
                logger.info('mbet.created_date:' + str(mbet.created_date))
            else:
                # check if a player has already bet on that match 
                mbet_temp           = MatchBet.objects.filter( match_id = form.cleaned_data['match_id'] ).filter( player_id = user )
                if mbet_temp: 
                    # If bet exists, user must be redirect to the update form
                    return HttpResponseRedirect( reverse('bets:mbet_detail', args=(mbet_temp[0].id,)))
                mbet                = MatchBet()
                mbet.player_id      = user
                mbet.match_id       = form.cleaned_data['match_id']
                mbet.created_date   = timezone.now()
                logger.info('mbet_id is empty, so this is insert')

            mbet.home_team_score    = form.cleaned_data['home_team_score']
            mbet.home_team_tries    = form.cleaned_data['home_team_tries']
            mbet.home_team_bonus    = form.cleaned_data['home_team_bonus']
            mbet.away_team_score    = form.cleaned_data['away_team_score']
            mbet.away_team_tries    = form.cleaned_data['away_team_tries']
            mbet.away_team_bonus    = form.cleaned_data['away_team_bonus']
            mbet.card               = form.cleaned_data['card']
            mbet.drop_goal          = form.cleaned_data['drop_goal']
            mbet.fight              = form.cleaned_data['fight']
            mbet.modified_date      = timezone.now()
            mbet.save()
            return HttpResponseRedirect( reverse('bets:mbet_detail', args=(mbet.id,)))
        return render( request, 'bets/bet_form.html', { 'form': form } )
    else:
        """
        GET with matchBet_id => update a bet => check exists bet
        else diplay an empty form 
        """
        params  = dict()
        if mbet_id:
            # TODO check if username == matchBet_id
            username    = request.user.username
            mbet        = get_object_or_404(MatchBet, pk=mbet_id)
            if mbet.player_id.username == username:
                # this is the owner, you can fill the form
                form                = MatchBetForm( instance=mbet )
                params['form']      = form
                params['elt']       = "matchBet"
                #params['post_url']  = "bets:mbet_add"
                params['post_url']  = reverse( 'bets:mbet_add', args=(tournament_id, mbet_id))
                return render( request, 'bets/bet_form.html', params)
        form    = None
        if m_id:
            match       = Match.objects.get( id = m_id )
            if match:
                form    = MatchBetForm( initiate = { 'match_id': match } )
        if form is None: 
            form                = MatchBetForm()
        params['form']      = form
        params['elt']       = "matchBet"
        #params['post_url']  = "'bets:mbet_add' "+tournament_id
        params['post_url']  = reverse( 'bets:mbet_add', args=(tournament_id) )
        return render( request, 'bets/bet_form.html', params)

@require_http_methods(["GET", "POST"])
def tournamentBet_add( request, tournament_id, tbet_id=None ):
    if request.method == 'POST':
        user         = User.objects.get(username=request.user.username)
        tournament  = get_object_or_404(Tournament, pk=tournament_id)
        form         = TournamentBetForm(request.POST, tournament_id = tournament_id)
        if form.is_valid():
            if tbet_id is not None:
                # TODO Do not let save a tournament bet if an user has already his one
                tbet                = get_object_or_404(TournamentBet, pk=tbet_id)
                logger.info('tbet_id is present, so this is update')                
            else:
                tbet                = TournamentBet()   
                tbet.player_id      = user
                tbet.tournament_id  = tournament
                tbet.created_date   = timezone.now()
                logger.info('tbet_id is empty, so this is insert')
            tbet.first_team     = form.cleaned_data['first_team']
            tbet.second_team    = form.cleaned_data['second_team']
            tbet.third_team     = form.cleaned_data['third_team']
            tbet.fourth_team    = form.cleaned_data['fourth_team']
            tbet.fifth_team     = form.cleaned_data['fifth_team']
            tbet.sixth_team     = form.cleaned_data['sixth_team']
            tbet.grand_slam     = form.cleaned_data['grand_slam']
            tbet.wooden_spoon   = form.cleaned_data['wooden_spoon']
            tbet.modified_date  = timezone.now()
            tbet.save()
            return HttpResponseRedirect( reverse('bets:tbet_detail', args=(tbet.id,)))
        return render( request, 'bets/bet_form.html', { 'form': form } )
    else:
        """
        GET with tournamentBet_id => update a bet => check exists bet
        else diplay an empty form 
        """
        params  = dict()
        if tbet_id:
            # TODO check if username == matchBet_id
            username    = request.user.username
            tbet        = get_object_or_404(TournamentBet, pk=tbet_id)
            if tbet.player_id.username == username:
                # this is the owner, you can fill the form
                form                = TournamentBetForm( instance=tbet, tournament_id = tournament_id )
                params['form']      = form
                params['elt']       = "tournamentBet"
                params['post_url']  = reverse( 'bets:tbet_add', args=(tournament_id, tbet_id ) )
                #params['post_url']  = "bets:tbet_add"
                return render( request, 'bets/bet_form.html', params)
        form                = TournamentBetForm( tournament_id = tournament_id )
        params['form']      = form
        params['elt']       = "tournament Bet"
        params['post_url']  = reverse( 'bets:tbet_add', args=( tournament_id) )
        return render( request, 'bets/bet_form.html', params)

"""
List every tournament by year
if there is only one tounament redirect to tbet_list
"""
def bet_index( request ): 
    # TODO 
    # disable links if tournament hasn't started
    logger.info('Welcome to bets module')
    params          = dict()
    tournament_list = Tournament.objects.order_by( '-year' )
    if len( tournament_list ) == 1:
        return HttpResponseRedirect( reverse('bets:tbet_list', args=[tournament_list[0].id] ) )
        #return HttpResponseRedirect( reverse('bets:tbet_list', args=(tbet_list[0].id,)))
    params['tournament_list' ]  = tournament_list
    return render( request, 'bets/tournament_list.html', params )

"""
This view display only available match of a tournament
"""
def mbet_available( request, tournament_id ):
    logger.info('Welcome to available bets')
    params      = {'error_message': None, 'is_update': None }
    tournament  = get_object_or_404(Tournament, pk=tournament_id)
    matchs      = Match.objects.filter( tournament_id = tournament_id )
    params['tournament']    = tournament
    params['match_list']    = matchs
    return render( request, 'bets/mbet_available', params )
    

"""
List every tournament bets 
if tournament hasn't yet started : 
- if user has already placed a bet, display countdown
- else ask him if he wants to place a bet
"""
@login_required
def tbet_list( request, tournament_id ):
    params      = {'error_message': None, 'is_update': None }
    tbet_list   = TournamentBet.objects.filter( tournament_id = tournament_id )
    # TODO deny acces before the begining of the tournament
    # select every matchs of the tournament and get the date of first one
    # if date.now() is lower than the match date, display message
    # wrong because I added a "begins" field in tournament model
    # DONE
    # This is done by adding a new field in tournament model : "begins"
    tournament  = Tournament.objects.get( id = tournament_id)
    params['tournament']    = tournament
    if tournament.begins < timezone.now():
        params['tbet_list'] = tbet_list
    else:
        # If user has not yet placed a bet, propose him
        # else display message
        user        = User.objects.get( username = request.user.username )
        countdown   = tournament.begins - timezone.now()
        message = "The tournament has not yet started, Access available in %s - %s - %s" % ( (str(countdown), str(tournament.begins), str(timezone.now()) ) )
        has_bet = False
        for t in tbet_list:
            if t.player_id.id == user.id:
                # The player has already bet
                params['message']       = "You have to wait until Tournament begins: " + str(countdown)
                params['tbet_button_title']  = "Uptade your Bet "
                params['tbet_button_url']    = reverse( "bets:tbet_add", args=(t.tournament_id.id, t.id))
                has_bet = True
        if not has_bet :
            params['message']       = "The tournament will start in %s, would you like to place a ranking bet ? " % (str(countdown))
            params['tbet_button_title']  = "Place a ranking bet"
            params['tbet_button_url']    = reverse( 'bets:tbet_add', args=(tournament_id) )

    # Add a button to place a match bet
    
    params['mbet_button_title'] = "Add a match bet"
    params['mbet_button_url']   = reverse( 'bets:mbet_add', args=( tournament_id ) )
        
    return render( request, 'bets/tbet_list.html', params )

"""
This view display every information of a tournament bet
"""
def tbet_detail( request, tbet_id ):
    params      = dict()
    tbet        = get_object_or_404(TournamentBet, pk=tbet_id)
    tbetform    = TournamentBetForm( instance=tbet )
    username    = request.user.username 
    # Check if update is yet possible tournnament.begins > timezone.now()
    tournament  = Tournament.objects.get( id = tbet.tournament_id.id )
    if tournament and tournament.begins > timezone.now():
        params['is_update']     = True
        params['update_url']    = reverse( 'bets:tbet_add', args=(tournament.id, tbet.id))

    if tbet.player_id.username == username:
        params['bet']  = tbetform
        params['elt']   = 'tournamentBet'
        return render( request, 'bets/bet_detail.html', params)
    else:
        params["message"]   = "You are not allowed to see this page"
        return render( request, 'bets/bet_detail.html', params )

"""
This view display every bet of a tournament
"""
def mbet_list( request, tbet_id ):
    # TODO 
    # Display oinly matchs information if matchs hasn't started
    mbet_list   = MatchBet.objects.filter( tournament_id = tbet_id )
    params     = { 'bet_list': mbet_list }
    return render( request, 'bets/bet_list.html', params )

"""
This view display every information of a match bet 
"""
def mbet_detail( request, mbet_id ):
    params      = {'error_message': None, 'is_update': None }
    mbet        = get_object_or_404(MatchBet, pk=mbet_id)
    mbetform    = MatchBetForm( instance=mbet )
    username    = request.user.username 
    match       = Match.objects.get( id=mbet.match_id.id)
    if match is not None:
        if match.date > timezone.now():
            params['update'] = True
            params['update_url' ] = reverse( 'bets:mbet_add', args=(match.tournament_id.id, mbet_id,))
    if mbet.player_id.username == username:
        params['bet']  = mbetform
        params['elt']   = 'matchBet'
        return render( request, 'bets/bet_detail.html', params)
    else:
        params["message"]   = "You are not allowed to see this page"
        return render( request, 'bets/bet_detail.html', params )

"""
This view display all bets by match and round
"""
@login_required
def prognosis( request ):
    params      = {'error_message': None, 'is_update': None }
    match       = Match.objects.filter(date__lte=timezone.now())
    mbet        = MatchBet.objects.all()
    params['match'] = match
    params['bet']   = mbet
    return render(request, 'bets/prognosis.html', params)
    
#class BetView( View )
