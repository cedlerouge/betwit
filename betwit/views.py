from __future__ import unicode_literals

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View

from tournaments.models import Tournament
from andablog.models import Entry
import tournaments.board
import datetime
from django.db.models import Q


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):

        content = {

            # Blog
            'entries':  Entry.objects.filter(Q(is_published=True) | Q(author__isnull=False))
            #comments = Comment.objects.last(5)

            # tournament
            #tid = Tournament.objects.filter(state=1,year=datetime.now().year)
            #results = tournaments.board.getTeamTable(tid)



        }

        return render(request, self.template_name, { 'content': content })
