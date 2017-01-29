from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^$', views.tournament_list, name='tournament_list' ),
    url( r'^tournament/add/$', views.tournament_form, name='tournament_form' ),
    url( r'^tournament/(?P<tournament_id>[0-9]+)/$', views.match_list_by_tournament, name = "match_list_by_tournament" ),
    url( r'^tournament/(?P<tournament_id>[0-9]+)/match_add/$', views.match_form, name='match_form' ),
    url( r'^team/$', views.team_list, name="team_list" ),
    url( r'^team/add/$', views.team_form, name='team_form' ),
    url( r'^team/(?P<team_id>[0-9]+)/$', views.team_detail, name = "team_detail" ),
    url( r'^match/$', views.match_list, name='match_list' ),
    url( r'^match/(?P<match_id>[0-9]+)/$', views.match_detail, name = "match_detail" ),
]
