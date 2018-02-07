from __future__ import unicode_literals

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View

from tournaments.models import Tournament
from andablog.models import Entry
import tournaments.board
import datetime
from django.db.models import Q

class Index(View):
    def get(self, request):
        #return HttpResponse('I am called from a get Request')
        return render(request, 'base.html')
    def post(self, request):
        #return HttpResponse('I am called from a post Request')
        return render(request, 'base.html')

class Rules(View):
    def get(self, request):
        return render(request, 'rules.html')

class Apropos(View):
    def get(self, request):
        return render(request, 'apropos.html')

class Players(View):
    def get(self, request):
        if request.user.is_authenticated(): 
            return render(request, 'slides.html')
        else:
            return HttpResponseRedirect('/accounts/login/')

class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        limit = 1
        tid = Tournament.objects.filter(state=1,year=datetime.datetime.now().year)
        content = {

            # Blog
            'entries':  Entry.objects.filter(Q(is_published=True) | Q(author__isnull=False)).order_by('-published_timestamp'),
            #comments = Comment.objects.last(5)

            # tournament
            'team_stats': tournaments.board.getTeamTable(tid)



        }

        return render(request, self.template_name, { 'content': content })
