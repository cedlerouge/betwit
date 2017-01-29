from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

from .models import Tournament, Match, Team, MatchPoint
from .forms import TeamForm, TournamentForm, MatchForm, MatchPointForm

# Create your views here.

def tournament_list( request ):
    tournament_list = Tournament.objects.order_by( '-year' )
    context         = { 'tournament_list':tournament_list }
    return render( request, 'tournaments/tournament_list.html', context )

def tournament_form( request ):
    form    = TournamentForm()
    return render( request, 'tournaments/tournament_form.html', { 'elt': 'tournament', 'form': form } )

def team_list( request ):
    team_list       = Team.objects.order_by( 'name' )
    context         = { 'team_list':team_list }
    return render( request, 'tournaments/team_list.html', context )

def team_detail( request, team_id ):
    team            = get_object_or_404( Team, pk=team_id )
    return render( request, 'tournaments/team_detail.html', { 'team':team } )

def team_form( request ):
    form    = TeamForm()
    return render( request, 'tournaments/tournament_form.html', { 'elt': 'team', 'form': form } )

def match_list( request ):
    match_list      = Match.objects.order_by( '-date' )
    context         = { 'match_list':match_list }
    return render( request, 'tournaments/match_list.html', context )

def match_list_by_tournament( request, tournament_id ):
    match_list      = get_object_or_404( Match, pk=tournament_id )
    context         = { "match_list":match_list }
    return render( request, 'tournaments/match_list.html', context )

def match_detail( request, match_id ):
    match           = get_object_or_404( Match, pk=match_id )
    return render( request, 'tournaments/match_detail.html', { 'match':match } )

def match_form( request ):
    form    = MatchForm()                                                    
    return render( request, 'tournaments/tournament_form.html', { 'elt': 'match', 'form': form } )

#@login_required
def team_add( request ):
    form    = TeamForm(request.POST)
    if form.is_valid():
        name            = form.clean_data['name']
        nationality     = form.clean_data['nationality']
        # TODO login_required
        # author          = request.user.username
        # created_date    = datetime.datetime.now()
        # TODO add logo and thumbnail
        #logo    = ImageModel( logo = request.FILES['logo'] )
        team    = Team()
        team.name   = name
        team.nationality    = nationality
        team.save()
        return HttpResponseRedirect( reverse('tournaments:team_detail', args=(team.id,)))
    return render( request, 'tournaments/team_detail.html', { 'team': team } )
        
        
