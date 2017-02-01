from django.forms import ModelForm, Textarea
from django import forms
from bets.models import MatchBet,TournamentBet, BetPoint

class MatchBetForm( ModelForm ):
    """
    MatchBet form to place a bet on a match
    """
    class Meta:
        model   = MatchBet
        exclude = ['player_id', 'points_won']

class TournamentBetForm( ModelForm ):
    """
    TournamentBet form which will be closed at the begining of the first match
    """
    class Meta:
        model   = TournamentBet
        exclude = ['player_id', 'points_won', 'created_date', 'modified_date']

class BetPointForm( ModelForm ):
    class Meta:
        model   = BetPoint
        fields  = '__all__'
