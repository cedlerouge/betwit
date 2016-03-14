from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from user_profile.models import User
from matchs.models import Match
from models import Bet, BetCup
from forms import BetForm, BetCupForm

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import logging
logger = logging.getLogger('django')

from django.utils import timezone


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class Logout(View):
  def get(self, request):
    logout(request)
    return redirect('home')

class Login(View):
  def get(self, request):
    params	= dict()
    return render(request, 'login.html', params)

  def post(self, request):
    params   = dict()
    errors   = list()
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/user/'+username+'/')
      else:
        errors.append("Ce compte est desactiv&eacute;")
        params['errors']	= errors
        return render(request, 'login.html', params)
    else:
      errors.append("Le login et le mot de passe ne correspondent pas.") 
      errors.append("Veuillez essayer retenter de vous connecter")
      params['errors'] 		= errors
      return render(request, 'login.html', params)
        

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
      logger.info('authorized user')
      return HttpResponseRedirect('/user/'+request.user.username)
    else:
      logger.info('unauthorized user')
      return HttpResponseRedirect('/login/')


class Profile(View):
  """
  User profile reachable from /user/<username>/ URL
  """
  def get(self, request, username):
    params 	= dict()
    userProfile	= User.objects.get(username=username)
    bets 	= Bet.objects.filter(user=userProfile)
    betcup      = BetCup.objects.filter(user=userProfile)
#    for obj in betcup:
#        obj.fields = dict((field.name, field.value_to_string(obj))
#                                            for field in obj._meta.fields)
#    form	= BetForm()
    params['bets'] = bets
    params['user'] = userProfile
    params['betcup'] = betcup
    return render(request, 'profile.html', params)

class PostBet(LoginRequiredMixin,View):
  def get(self, request, username):
    params              =  dict()
    errors		= list()
    user                = User.objects.get(username=username)
    # get list of bets by user to avoid betting twice on the same match
    #bets        	= Bet.objects.filter(user=user)
    #idOfBetMatch	= [ obj.match.id for obj in bets ]
    # get all match to know which one to present on form
    #matchs		= Match.objects.all()
    #matchsToBet		= [(None, '-- choose a match --'), ]
    #for m in matchs:
    #  if timezone.now() < m.match_date and m.id not in idOfBetMatch:
    #   matchsToBet.append( (m.id, m.teamA + ' vs ' + m.teamB) )
    #betcup      	= BetCup.objects.filter(user=user)

    form                = BetForm( user = user )
    #form		= BetForm()
    #form.match_choices  = matchsToBet
    params['user']      = user
    params['form']      = form
    return render(request, 'betcup.html', params)


  """ Match Post form available on page /user/<username> URL"""
  def post(self, request, username):
    user	= User.objects.get(username=username)
    form	= BetForm(self.request.POST, user=user)
    if form.is_valid():
      match     = Match.objects.get(id=form.cleaned_data['match'])
      print 'form = %r' % form
      bet	= Bet(
                    user 	= user,
                    match 	= match,
                    scoreA	= form.cleaned_data['scoreA'],
                    scoreB 	= form.cleaned_data['scoreB'],
                    triesA 	= form.cleaned_data['triesA'],
                    triesB 	= form.cleaned_data['triesB'],
                    card	= form.cleaned_data['card'],
                    drop_goal   = form.cleaned_data['drop_goal'],
                    fight       = form.cleaned_data['fight'],
                    created_date= timezone.now()
                  )
      bet.save()
      return HttpResponseRedirect('/user/'+username+'/')
    else:
      print 'form = %r' % form
      return render(request, 'betcup.html', {'form': form})


class PostBetCup(LoginRequiredMixin,View):
  def get(self, request, username):
    params		=  dict()
    user		= User.objects.get(username=username)
    betcup      	= BetCup.objects.filter(user=user)    
    errors		= list()
    if len( betcup ) > 0 :
        errors          = {"Vous avez deja un pari d'avant tournoi"}
        params["errors"] = errors
        return render(request, "betcup.html", params)
    else:
        form		= BetCupForm()
        params['user']	= user
        params['form']	= form
        return render(request, 'betcup.html', params)

  """
  Bet Cup Post form available on page /user/<username/betcup URL
  """
  def post(self, request, username):
    form = BetCupForm(self.request.POST)
    if form.is_valid():
      user	= User.objects.get(username=username)
      bet_cup	= BetCup(
                    user	= user,
                    first	= form.cleaned_data['first'],
                    second      = form.cleaned_data['second'],
                    third       = form.cleaned_data['third'],
                    fourth      = form.cleaned_data['fourth'],
                    fifth       = form.cleaned_data['fifth'],
                    sixth       = form.cleaned_data['sixth'],
                    grand_slam	= form.cleaned_data['grand_slam'],
                    wooden_spoon= form.cleaned_data['wooden_spoon'],
                    created_date= timezone.now()
                  )
      bet_cup.save()
      return HttpResponseRedirect('/user/'+username+'/')
    else:
      return render(request,'betcup.html', {'form': form})


class BetRanking(View):
  def get(self, request):
    params		= dict()
    users		= User.objects.all()
    rank		= list()
    for user in users: 
      bets	= Bet.objects.filter(user = user.id)
      score	= sum(int(b['points_won']) for b in bets.values())
      # find best score per prognosis
      best_score = 0
      for b in bets.values():
        if best_score <= int(b['points_won']): 
          best_score = int(b['points_won'])
      rank.append( (user.username, score, best_score) )
    rank.sort(key=lambda r: r[1], reverse=True)
    params['rank']	= rank
    return render(request, 'rank.html', params)
    

class BetRules(View):
  def get(self, request):
    params		= dict()
    return render(request, 'rules.html', params)


class BetPrognosis(View):
  def get(self, request):
    params		= dict()
    match		= Match.objects.filter(match_date__lte=timezone.now())
    bets        	= Bet.objects.all()
    params['match']	= match
    params['bets']	= bets
    return render(request, 'prognosis.html', params)
