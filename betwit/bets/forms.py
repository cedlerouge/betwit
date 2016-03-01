
from django import forms
from django.core.validators import MinValueValidator
from matchs.models import Match
from bets.models import Bet
from django.utils import timezone

class BetForm(forms.Form):
   
    match_choice	= [(None, '-- choose a match --'), ]   
    #match_choice	= []
    match	= forms.ChoiceField(
	choices 	= match_choice, 
	widget 		= forms.Select(),#attrs = {'class':"form-control"}), 
	help_text 	= "In first select the match")
    scoreA	= forms.IntegerField(
	initial		= 0, 
	validators	= [MinValueValidator(0)], 
	error_messages	= {'No negative': 'I have never seen such a score !'},
	#widget 		= forms.NumberInput(attrs = {'class': 'form-control'})
	)
    scoreB      = forms.IntegerField(
	initial		= 0, 
	validators	= [MinValueValidator(0)], 
	error_messages	= {'No negative': 'I have never seen such a score !'},
	#widget          = forms.NumberInput(attrs = {'class': 'form-control'})
	)
    triesA      = forms.IntegerField(
	initial		= 0, 
	validators	= [MinValueValidator(0)], 
	error_messages	= {'No negative': 'Please explain me how it possible'},
	#widget          = forms.NumberInput(attrs = {'class': 'form-control'})
	)
    triesB      = forms.IntegerField(
	initial		= 0, 
	validators	= [MinValueValidator(0)], 
	error_messages	= {'No negative': 'Please explain me how it possible'},
	#widget          = forms.NumberInput(attrs = {'class': 'form-control'})
	)
    card	= forms.BooleanField(
	required	= False, 
	initial		= False,
	#widget          = forms.CheckboxInput(attrs = {'class': 'form-control'})
	)
    drop_goal	= forms.BooleanField(
	required	= False, 
	initial		= False,
	#widget          = forms.CheckboxInput(attrs = {'class': 'form-control'})
	)
    fight	= forms.BooleanField(
	required	= False, 
	initial		= False,
	#widget          = forms.CheckboxInput(attrs = {'class': 'form-control'})
	)

    def __init__(self, *args, **kwargs):
        # to avoid betting twice on the same match and on past matchs
        # get the user from the view
        user		= kwargs.pop('user', None)
        match_choice	= [(None, '-- choose a match --'), ]
        if user is not None: 
            # get all user's bets already done
            bets		= Bet.objects.filter(user=user)
            idOfBetMatch        = [ obj.match.id for obj in bets ]
            matchs              = Match.objects.all()
            for m in matchs:
                # checks that match is not already played
                if timezone.now() < m.match_date and m.id not in idOfBetMatch:
                    match_choice.append( (m.id, m.teamA + ' vs ' + m.teamB) )
        super(BetForm, self).__init__(*args, **kwargs)
        self.fields['match'] = forms.ChoiceField(
		choices	= match_choice, 
		widget	= forms.Select(),#attrs = {'class':"form-control"}), 
		help_text = "In first select the match"
		)


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
