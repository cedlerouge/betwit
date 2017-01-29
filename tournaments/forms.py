from django.forms import ModelForm, Textarea
from django import forms
from tournaments.models import Team,Tournament, Match, MatchPoint


class TeamForm( ModelForm ):
    """ 
    Team form with upload image
    """
    class Meta:
        model   = Team
        fields  = ['name', 'nationality', 'logo']

class TournamentForm( ModelForm ):
    # control the field year by using choices instead of integer field 
    year = forms.ChoiceField(choices=[(x, x) for x in range(1900, 2000)], required=False)

    class Meta:
        model   = Tournament
        fields  = [ 'name', 'year' ]

class MatchForm( ModelForm ):
    
    class Meta:
        model   = Match
        fields  = [ 'date', 'home_team_id', 'away_team_id' ]


class MatchPointForm( ModelForm ):
    class Meta:
        model   = MatchPoint
        fields  = '__all__'
