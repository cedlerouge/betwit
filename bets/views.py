from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from operator import attrgetter, itemgetter
import datetime

from tournaments.models import Tournament, Match, Team
from .models import MatchBet, TournamentBet, BetPoint, MatchRating
from .forms import MatchBetForm, TournamentBetForm, BetPointForm, ProfileForm, UserForm



import logging
logger = logging.getLogger('bets')
logger.addHandler( logging.StreamHandler() )
logger.info('This is bets/views')
logger.info('me vois tu ?   ')

# Create your views here.# Create your views here.

class UserRedirect(View):
    def get(self, request):
        if request.user.is_authenticated():
            # TODO mettre en place des logs
            #logger.info('authorized user')
            return HttpResponseRedirect(request.user.username)
        else:
            #logger.info('unauthorized user')
            return HttpResponseRedirect('/accounts/login/')


class UserProfile(View):
    """
    User profile reachable from /user/<username>/ URL
    """

    # TODO @login_required <--- https://docs.djangoproject.com/en/1.10/topics/class-based-views/intro/#decorating-class-based-views
    def get(self, request, username=None):
        params          = {'error_message': None }
        user            = None
        is_his_own      = False
        user_share      = False

        """ 2 choices :
        * display information => /accounts/settings
        * display form to update settings => accounts/settings/update
        """
        if "profile" in request.path:
            logger.info(" je suis dans update: " + request.user.username )
            if request.user.username:
                user_form       = UserForm(instance=request.user)
                profile_form    = ProfileForm(instance=request.user.profile)
                params['userForm']      = user_form
                params['profileForm']   = profile_form
            else:
                params['error_message'] =  "You must be authenticated"

            return render(request, 'bets/profile_form.html', params)

        else:
            """
            if the user's profile :
                display all information and modify button
            else:
                display only what the user wants to share
            """
            if request.user.username :
                user            = User.objects.get(username = request.user.username)
            params['user']  = user
            # TODO manage the user profile display for other visitors
            #if username == request.user.username:
            #    is_his_own = True
            #    user_share = True
            #else:
            #    if user.userprofile.allow_share :
            #        user_share = True
            return render(request, 'bets/settings.html', params)

    def post(self, request, username=None):
        params          = {'error_message': None }
        user_form       = UserForm(request.POST, instance=request.user)
        profile_form    = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('settings'))
        else:
            return render(request, 'bets/profile_form.html', params)


class MyBets(View):
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
            tournamentBet   = TournamentBet.objects.filter( tournament=t ).filter( player = userProfile ).first()
            if tournamentBet:
                tbetForm    = TournamentBetForm( instance=tournamentBet )
                match       = Match.objects.filter( tournament=t )
                for m in match :
                    matchBet = None
                    matchBet    = MatchBet.objects.filter( match = m ).filter( player = userProfile ).first()
                    if matchBet:
                        lm.append(matchBet)
        if not tournamentBet:
            return HttpResponseRedirect( reverse('bets:tbet_add', args=[t.id] ) )

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
        return render(request, 'bets/mybets.html', params)


class BetRanking(View):
  def get(self, request):
    params      = dict()
    users       = User.objects.all()
    rank        = list()
    rankf       = list()
    for user in users:
      # TODO filter parmi les tournois
      bet_points        = BetPoint.objects.filter(player = user)
      tournament_bets   = TournamentBet.objects.filter(player = user).last()
      score     = sum(float(b['points_won'] if b['points_won'] is not None else 0 ) for b in bet_points.values())
      try:
        # if tournament_bets != Null
        scoref    = score + tournament_bets.points_won
      except:
        scoref    = score
      rankf.append((user.username, scoref))
      # find best score per prognosis
      best_score = 0
      for b in bet_points.values():
        if best_score <= float(b['points_won'] if b['points_won'] is not None else 0):
          best_score = float(b['points_won'] if b['points_won'] is not None else 0)
      rank.append( (user.username, score, best_score) )
    #rank.sort(key=lambda r: r[1], reverse=True)
    # https://wiki.python.org/moin/HowTo/Sorting
    rank.sort(key = itemgetter(1, 2), reverse = True)
    rankf.sort(key = itemgetter(1), reverse = True)
    r = zip(rank, rankf)
    params['rank']  = r
    return render(request, 'bets/rank.html', params)

@login_required
@require_http_methods(["GET", "POST"])
def matchBet_add( request, tournament_id=None, mbet_id=None, m_id=None ):
    logger.info("matchbet")
    params          = {'error_message': None, 'is_update': None }
    if request.method == 'POST':
        user        = User.objects.get(username=request.user.username)
        form        = MatchBetForm(request.POST)
        #if form.fields['match'] is not None:
        #    mid = str(form.data.match)
        #    form.fields['match'] = forms.ModelChoiceField(queryset=Match.objects.filter( id = mid ) )
            #form.fields['match'].value = Match.objects.get( id = mid )
        logger.info (" je suis le formulaire poste de matchbet_add: ", str(form.fields))
        if form.is_valid():
            if mbet_id is not None:
                # TODO Do not let save a match bet if an user has already his one for a specified match id
                mbet = get_object_or_404(MatchBet, pk=mbet_id)
                logger.error('mbet_id is present, so this is update')
                logger.info('mbet.id:' + str(mbet.id))
                logger.info('mbet.home_team_score:' + str(mbet.home_team_score))
                logger.info('mbet.created_date:' + str(mbet.created_date))
            else:
                # check if a player has already bet on that match
                mbet_temp           = MatchBet.objects.filter( match = form.cleaned_data['match'] ).filter( player = user )
                if mbet_temp:
                    # If bet exists, user must be redirect to the update form
                    return HttpResponseRedirect( reverse('bets:mybets'))
                mbet                = MatchBet()
                mbet.player         = user
                mbet.match          = form.cleaned_data['match']
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
            mbet.jokerbet_value     = form.cleaned_data['jokerbet_value']
            mbet.modified_date      = timezone.now()
            mbet.save()
            return HttpResponseRedirect( reverse('bets:mybets'))
        return render( request, 'bets/bet_form.html', { 'form': form } )
    else:
        """
        GET with matchBet_id => update a bet => check exists bet
        else diplay an empty form
        """
        #params  = dict()
        if mbet_id:
            # TODO check if username == matchBet_id
            username    = request.user.username
            mbet        = get_object_or_404(MatchBet, pk=mbet_id)
            if mbet.player.username == username:
                # this is the owner, you can fill the form
                match               = Match.objects.get( id = mbet.match.id)
                jokerbet_text       = match.jokerbet_text
                form                = MatchBetForm( instance=mbet,  initial = {'match': match, 'jokerbet_text': "Pari Surprise : " + jokerbet_text} )
                params['form']      = form
                params['elt']       = "matchBet"
                params['is_update'] = True
                params['post_url']  = reverse( 'bets:mbet_add_post_mid', args=(tournament_id, mbet_id))
                return render( request, 'bets/bet_form.html', params)
        form    = None
        if m_id:
            # match is set because
            match       = Match.objects.get( id = m_id )
            if match:
                jokerbet_text = Match.objects.get(id = m_id).jokerbet_text
                form    = MatchBetForm( initial = { 'match': match, 'jokerbet_text': "Pari Surprise : " + jokerbet_text } )
                #logger.error("m_id is set ans match is not none => form : " + str(form))
        if form is None:
            #logger.error("form is none so matchbetform with tid")
            form                = MatchBetForm( tournament = tournament_id)
            #logger.error("tid: " + str(tournament_id))
        params['form']      = form
        params['elt']       = match.home_team.name + " vs " + match.away_team.name
        #params['post_url']  = "'bets:mbet_add' "+tournament_id
        params['post_url']  = reverse( 'bets:mbet_add_mid', args=(tournament_id, m_id) )
        return render( request, 'bets/bet_form.html', params)

@login_required
@require_http_methods(["GET", "POST"])
def tournamentBet_add( request, tournament_id, tbet_id=None ):
    if request.method == 'POST':
        user         = User.objects.get(username=request.user.username)
        tournament  = get_object_or_404(Tournament, pk=tournament_id)
        form         = TournamentBetForm(request.POST, tournament = tournament_id)
        if form.is_valid():
            if tbet_id is not None:
                # TODO Do not let save a tournament bet if an user has already his one
                tbet                = get_object_or_404(TournamentBet, pk=tbet_id)
                logger.info('tbet_id is present, so this is update')
            else:
                tbet                = TournamentBet()
                tbet.player         = user
                tbet.tournament     = tournament
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
            if tbet.player.username == username:
                # this is the owner, you can fill the form
                form                = TournamentBetForm( instance=tbet, tournament = tournament_id )
                params['form']      = form
                params['elt']       = "tournamentBet"
                params['post_url']  = reverse( 'bets:tbet_add', args=(tournament_id, tbet_id ) )
                #params['post_url']  = "bets:tbet_add"
                return render( request, 'bets/bet_form.html', params)
        form                = TournamentBetForm( tournament = tournament_id )
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
    # TODO Need better management of tournamentS
    #if len( tournament_list ) == 1:
    #    return HttpResponseRedirect( reverse('bets:tbet_list', args=[tournament_list[0].id] ) )
    #    #return HttpResponseRedirect( reverse('bets:tbet_list', args=(tbet_list[0].id,)))
    params['tournament_list' ]  = tournament_list
    return render( request, 'bets/tournament_list.html', params )

"""
This view display only available match of a tournament
"""
def mbet_available( request, tournament_id=0 ):
    logger.info('Welcome to available bets')
    params      = {'error_message': None, 'is_update': None }
    if tournament_id != 0: 
        tournament  = get_object_or_404(Tournament, pk=tournament_id)
    else:
        tournament  = Tournament.objects.all().order_by( '-year' )[0]
        tournament_id = tournament.id
    #matchs      = Match.objects.filter( tournament = tournament_id ).filter( date__gte = timezone.now( ))
    matchs      = Match.objects.filter( tournament = tournament_id )
    params['tournament']    = tournament
    params['match_list']    = matchs
    params['date_now']      = timezone.now()
    return render( request, 'bets/mbet_available.html', params )


"""
List every tournament bets
if tournament hasn't yet started :
- if user has already placed a bet, display countdown
- else ask him if he wants to place a bet
"""
@login_required
def tbet_list( request, tournament_id ):
    params      = {'error_message': None, 'is_update': None }
    tbet_list   = TournamentBet.objects.filter( tournament = tournament_id )
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
            if t.player.id == user.id:
                # The player has already bet
                params['message']       = "You have to wait until Tournament begins: " + str(countdown)
                params['tbet_button_title']  = "Uptade your Bet "
                params['tbet_button_url']    = reverse( "bets:tbet_add", args=(t.tournament.id, t.id))
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
    tournament  = Tournament.objects.get( id = tbet.tournament.id )
    if tournament and tournament.begins > timezone.now():
        params['is_update']     = True
        params['update_url']    = reverse( 'bets:tbet_add', args=(tournament.id, tbet.id))

    if tbet.player.username == username:
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
    mbet_list   = MatchBet.objects.filter( tournament = tbet_id )
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
    match       = Match.objects.get( id=mbet.match.id)
    if match is not None:
        if match.date > timezone.now():
            params['update'] = True
            params['update_url' ] = reverse( 'bets:mbet_add', args=(match.tournament.id, mbet_id,))
    if mbet.player.username == username:
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
    params      = {'error_message': None, 'is_update': None, 'match': list(), 'bet':list() }
    tenabled    = Tournament.objects.get(state="1").id
    match       = Match.objects.filter(tournament=tenabled).filter(date__lte=timezone.now())
    # As rate is not stored in match, we must manipulate match object to display the rate of the match
    mid_list = []
    for m in match:
        mid_list.append(m.id)
        try :
            rate = MatchRating.objects.filter(match = m).last()
            if m.home_team_score > m.away_team_score:
                m.odds = rate.ht_rating 
            elif m.home_team_score < m.away_team_score:
                m.odds = rate.at_rating 
            else: 
                m.odds = rate.null_rating
        except:
            m.odds = 1
        params['match'].append(m)
    # TODO filter matchbets by tournament
    mbet        = MatchBet.objects.filter(match__in = mid_list)
    logger.error('match: ' + str(match))
    logger.error('mbet: ' + str(mbet))

    # like rate, we must manipulate matchbet object 
    # We can't save object althought rating will be add
    for b in mbet: 
        try:
            bp = BetPoint.objects.get(matchbet=b)
            b.points_won = bp.points_won
        except Exception,e :
            # if there is no betpoint for this bet, b.point_won = 0
            b.points_won = 0
        params['bet'].append(b)

    
    try:
        tbet        = TournamentBet.objects.filter(tournament = match[0].tournament)
        params['tournamentbets'] = tbet
    except Exception, e:
        logger.error("Get list of tournamentbet : " + str(e))
        params['tournamentbets'] = []
    #params['match'] = match
    #params['bet']   = mbet
    return render(request, 'bets/prognosis.html', params)


