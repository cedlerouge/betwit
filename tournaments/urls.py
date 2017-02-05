from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^$', views.tournament_list, name='tournament_list' ),
    url( r'^tournaments/add/$', views.tournament_add, name='tournament_add' ),
    url( r'^tournaments/(?P<tournament_id>[0-9]+)/$', views.tournament_detail, name = "tournament_detail" ),
    url( r'^tournaments/(?P<tournament_id>[0-9]+)/match_add/$', views.match_add, name='match_add' ),
    # TODO url( r'^tournament/(?P<tournament_id>[0-9]+)/team_add/$', views.team_add_to, name='team_add_to' ),
    url( r'^teams/$', views.team_list, name="team_list" ),
    url( r'^teams/add/$', views.team_add, name='team_add' ),
    #url( r'^team/team_add/$', views.team_add, name='team_add' ),
    url( r'^teams/(?P<team_id>[0-9]+)/$', views.team_detail, name = "team_detail" ),
    url( r'^matchs/$', views.match_list, name='match_list' ),
    url( r'^matchs/(?P<match_id>[0-9]+)/$', views.match_detail, name = "match_detail" ),
]
