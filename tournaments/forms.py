from django.forms import ModelForm, Textarea
from django import forms
#from bootstrap3_datetime.widgets import DateTimePicker
from tournaments.models import Team,Tournament, Match, MatchPoint

from datetime import datetime


class TeamForm( ModelForm ):
    """
    Team form with upload image
    """
    class Meta:
        model   = Team
        #fields  = ['name', 'nationality', 'logo']
        fields  = ['name', 'nationality' ]

class TournamentForm( ModelForm ):
    # control the field year by using choices instead of integer field
    currentYear = datetime.now().year
    year = forms.ChoiceField(choices=[(x, x) for x in range(2000,2033)], initial=currentYear, required=False)

    class Meta:
        model   = Tournament
        fields  = '__all__'
        #[ 'name', 'year' ]

class MatchForm( ModelForm ):
    class Meta:
        model   = Match
        fields  = [ 'date', 'home_team', 'away_team' ]


class MatchPointForm( ModelForm ):
    class Meta:
        model   = MatchPoint
        fields  = '__all__'
