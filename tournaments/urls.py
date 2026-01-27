from django.urls import path, re_path
from . import views

"""
L'application tournament affiche le dernier tournois actif (different de archived or comming)
dans cette page est affiche
* 2 onglets : equipe et resultats
* un bouton pour choisir un autre tournoi
"""

app_name = 'tournaments'

urlpatterns = [
    path('', views.tournament_list, name='tournament_list'),
    path('tournaments/', views.tournament_list, name='tournament_list'),
    re_path(r'^tournaments/(?P<tournament_id>[0-9]+)/$', views.tournament_detail, name='tournament_detail'),
    path('teams/', views.team_list, name='team_list'),
    re_path(r'^teams/(?P<team_id>[0-9]+)/$', views.team_detail, name='team_detail'),
    path('matchs/', views.match_list, name='match_list'),
    re_path(r'^matchs/(?P<match_id>[0-9]+)/$', views.match_detail, name='match_detail'),
]
