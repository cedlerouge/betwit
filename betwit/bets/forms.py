
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


class BetCupForm(forms.Form):

  teams_choice = (
      ('an', 'Angleterre'),
      ('ec', 'Ecosse'),
      ('fr', 'France'),
      ('ir', 'Irelande'),
      ('it', 'Italie'),
      ('pg', 'Pays de Galles'),
    )

  first		= forms.ChoiceField(choices=teams_choice, widget=forms.Select())
  second	= forms.ChoiceField(choices=teams_choice, widget=forms.Select())
  third		= forms.ChoiceField(choices=teams_choice, widget=forms.Select())
  fourth	= forms.ChoiceField(choices=teams_choice, widget=forms.Select())
  fifth		= forms.ChoiceField(choices=teams_choice, widget=forms.Select())
  sixth		= forms.ChoiceField(choices=teams_choice, widget=forms.Select())
  grand_slam	= forms.BooleanField(required=False, initial=False)
  wooden_spoon	= forms.BooleanField(required=False, initial=False)     
