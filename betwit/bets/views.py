from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
  if request.method == "GET":
    return HttpResponse('I am called from a get Request')
  elif request.method == "POST":
    return HttpResponse('I am called from a post Request')

