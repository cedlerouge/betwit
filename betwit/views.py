from __future__ import unicode_literals

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View



class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
         return render(request, self.template_name, {
            
        })
