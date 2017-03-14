from django.conf.urls import url
from . import views

"""
L'application tournament affiche le dernier tournois actif (different de archived or comming)
dans cette page est affiche
* 2 onglets : equipe et resultats
* un bouton pour choisir un autre tournoi
"""

urlpatterns = [
    url( r'^$', views.tournament_last, name='tournament_last' ),
    url( r'^tournaments/$', views.tournament_list, name='tournament_list' ),
    url( r'^tournaments/(?P<tournament_id>[0-9]+)/$', views.tournament_detail, name = "tournament_detail" ),
    #rl( r'^tournaments/(?P<tournament_id>[0-9]+)/match_add/$', views.match_add, name='match_add' ),
    # TODO url( r'^tournament/(?P<tournament_id>[0-9]+)/team_add/$', views.team_add_to, name='team_add_to' ),
    url( r'^teams/$', views.team_list, name="team_list" ),
    #rl( r'^teams/add/$', views.team_add, name='team_add' ),
    #url( r'^team/team_add/$', views.team_add, name='team_add' ),
    url( r'^teams/(?P<team_id>[0-9]+)/$', views.team_detail, name = "team_detail" ),
    url( r'^matchs/$', views.match_list, name='match_list' ),
    url( r'^matchs/(?P<match_id>[0-9]+)/$', views.match_detail, name = "match_detail" ),
]
