from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.generic import View

class Index(View):
  def get(self, request):
    return HttpResponse('I am called from a get Request')
  def post(self, request):
    return HttpResponse('I am called from a post Request')

