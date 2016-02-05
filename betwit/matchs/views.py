from django.shortcuts import render

# Create your views here.

from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from models import Match

class Results(View):
  def get(self, request):
    params      	= dict()
    matchs      	= Match.objects.order_by('match_date')
    params['matchs'] 	= matchs
    return render(request, 'results.html', params)
