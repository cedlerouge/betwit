from django.shortcuts import render

# Create your views here.

from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from user_profile.models import User
from matchs.models import Match
from models import Bet
from forms import BetForm

# for debug 
import pdb

class Index(View):
  def get(self, request):
    #return HttpResponse('I am called from a get Request')
    return render(request, 'base.html')
  def post(self, request):
    #return HttpResponse('I am called from a post Request')
    return render(request, 'base.html')

class Profile(View):
  """
  User profile reachable from /user/<username>/ URL
  """
  def get(self, request, username):
    params 	= dict()
    userProfile	= User.objects.get(username=username)
    bets 	= Bet.objects.filter(user=userProfile)
    form	= BetForm()
    params['bets'] = bets
    params['user'] = userProfile
    params['form'] = form
    return render(request, 'profile.html', params)

class PostBet(View):
  """ Match Post fomr available on page /user/<username> URL"""
  def post(self, request, username):
    form = BetForm(self.request.POST)
    if form.is_valid():
      user	= User.objects.get(username=username)
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
      return render(request, 'profile.html', {'form': form})
