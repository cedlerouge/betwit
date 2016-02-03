
from django import forms
from django.core.validators import MinValueValidator
from matchs.models import Match

class BetForm(forms.Form):
   
    match_choice	= [('', '-- choose a match --'), ] + [ (m.id, m.teamA + ' vs ' + m.teamB) for m in Match.objects.all()]  

    match	= forms.ChoiceField(choices=match_choice, widget=forms.Select(), help_text="In first select the match")
    scoreA	= forms.IntegerField(initial=0, validators=[MinValueValidator(0)], error_messages={'No negative': 'I have never seen such a score !'})
    scoreB      = forms.IntegerField(initial=0, validators=[MinValueValidator(0)], error_messages={'No negative': 'I have never seen such a score !'})
    triesA      = forms.IntegerField(initial=0, validators=[MinValueValidator(0)], error_messages={'No negative': 'Please explain me how it possible'})
    triesB      = forms.IntegerField(initial=0, validators=[MinValueValidator(0)], error_messages={'No negative': 'Please explain me how it possible'})
    card	= forms.BooleanField(required=False, initial=False)
    drop_goal	= forms.BooleanField(required=False, initial=False)
    fight	= forms.BooleanField(required=False, initial=False)
    
