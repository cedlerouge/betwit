from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import datetime

from .models import Tournament, Match, Team, MatchPoint
from .forms import TeamForm, TournamentForm, MatchForm, MatchPointForm

# Create your views here.

def tournament_list( request ):
    tournament_list = Tournament.objects.order_by( '-year' )
    context         = { 'tournament_list':tournament_list }
    return render( request, 'tournaments/tournament_list.html', context )

#def tournament_detail( request, tournament_id ):
#    tournament      = get_object_or_404( Tournament, pk=tournament_id )
#    #teams           = Team.objects.filter(
#    params          = dict()
#    matchs          = Match.objects.filter( tournament_id=tournament_id ).order_by( '-date' )
#    params['tournament'] = tournament
#    params['matchs'] = matchs
#    return render( request, 'tournaments/tournament_detail.html', params )
def tournament_detail( request, tournament_id ):
    tournament      = get_object_or_404( Tournament, pk=tournament_id )
    match_list      = Match.objects.filter( tournament_id = tournament_id )
    context         = { "tournament":tournament, "match_list":match_list }
    return render( request, 'tournaments/tournament_detail.html', context )

def tournament_form( request ):
    form    = TournamentForm()
    params['form']      = form
    params['elt']       = "tournament"
    params['post_url']  = reverse( 'tournaments:tournament_add' )
    return render( request, 'tournaments/tournament_form.html', params )

def team_list( request ):
    team_list       = Team.objects.order_by( 'name' )
    context         = { 'team_list':team_list }
    return render( request, 'tournaments/team_list.html', context )

def team_detail( request, team_id ):
    team            = get_object_or_404( Team, pk=team_id )
    return render( request, 'tournaments/team_detail.html', { 'team':team } )

#def team_form( request ):
#    form    = TeamForm()
#    return render( request, 'tournaments/tournament_form.html', { 'post_url': 'tournaments:team_add', 'form': form } )

def match_list( request ):
    match_list      = Match.objects.order_by( '-date' )
    context         = { 'match_list':match_list }
    return render( request, 'tournaments/match_list.html', context )

def match_detail( request, match_id ):
    match           = get_object_or_404( Match, pk=match_id )
    return render( request, 'tournaments/match_detail.html', { 'match':match } )

def match_form( request ):
    form    = MatchForm()                                                    
    return render( request, 'tournaments/tournament_form.html', { 'post_url': 'tournaments:match', 'form': form } )

#@login_required
@require_http_methods(["GET", "POST"])
def team_add( request ):
    if request.method == 'POST':
        form    = TeamForm(request.POST)
        if form.is_valid():
            name            = form.cleaned_data['name']
            nationality     = form.cleaned_data['nationality']
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
        return render( request, 'tournaments/tournament_form.html', { 'form': form } )
        
    else:
        form                = TeamForm()
        params              = dict()
        params['form']      = form
        params['elt']       = "team"
        params['post_url']  = reverse("tournaments:team_add")
        return render( request, 'tournaments/tournament_form.html', params ) 

@require_http_methods(["GET", "POST"])
def tournament_add( request ):
    if request.method == 'POST':
        form    = TournamentForm(request.POST)
        if form.is_valid():
            name        = form.cleaned_data['name']
            year        = form.cleaned_data['year']
            # TODO login_required
            # author          = request.user.username
            # created_date    = datetime.datetime.now()
            # TODO add logo and thumbnail
            #logo    = ImageModel( logo = request.FILES['logo'] )
            tournament      = Tournament()
            tournament.name = name
            tournament.year = year
            tournament.save()
            return HttpResponseRedirect( reverse('tournaments:tournament_detail', args=(tournament.id,)))
        return render( request, 'tournaments/tournament_form.html', { 'form': form } )

    else:
        form                = TournamentForm()
        params              = dict()
        params['form']      = form
        params['elt']       = "tournament"
        params['post_url']  = reverse("tournaments:tournament_add")
        return render( request, 'tournaments/tournament_form.html', params )

@require_http_methods(["GET", "POST"])
def match_add( request, tournament_id ):
    if request.method == 'POST':
        tournament  = get_object_or_404( Tournament, pk=tournament_id )
        form        = MatchForm(request.POST)
        if form.is_valid():
            # TODO login_required
            # author          = request.user.username
            # created_date    = datetime.datetime.now()
            # TODO add logo and thumbnail
            #logo    = ImageModel( logo = request.FILES['logo'] )
            match      = Match()
            match.tournament_id = tournament_id
            match.date          = form.cleaned_data['date']
            match.home_team_id  = form.cleaned_data['home_team_id']
            match.away_team_id  = form.cleaned_data['away_team_id']
            match.created_date  = timezone.now()
            match.save()
            return HttpResponseRedirect( reverse('tournaments:match_detail', args=(match.id,)))
        return render( request, 'tournaments/tournament_form.html', { 'form': form } )

    else:
        form                = MatchForm()
        params              = dict()
        params['form']      = form
        params['elt']       = "match"
        params['post_url']  = reverse("tournaments:match_add", args=(tournament_id))
        return render( request, 'tournaments/tournament_form.html', params )
