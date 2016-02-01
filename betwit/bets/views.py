from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.generic import View

from user_profile.models import User
from models import Bet

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
    params['bets'] = bets
    params['user'] = userProfile
    return render(request, 'profile.html', params)

