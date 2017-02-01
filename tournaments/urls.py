from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^$', views.tournament_list, name='tournament_list' ),
    url( r'^tournament/add/$', views.tournament_add, name='tournament_add' ),
    url( r'^tournament/(?P<tournament_id>[0-9]+)/$', views.tournament_detail, name = "tournament_detail" ),
    url( r'^tournament/(?P<tournament_id>[0-9]+)/match_add/$', views.match_add, name='match_add' ),
    # TODO url( r'^tournament/(?P<tournament_id>[0-9]+)/team_add/$', views.team_add_to, name='team_add_to' ),
    url( r'^team/$', views.team_list, name="team_list" ),
    url( r'^team/add/$', views.team_add, name='team_add' ),
    #url( r'^team/team_add/$', views.team_add, name='team_add' ),
    url( r'^team/(?P<team_id>[0-9]+)/$', views.team_detail, name = "team_detail" ),
    url( r'^match/$', views.match_list, name='match_list' ),
    url( r'^match/(?P<match_id>[0-9]+)/$', views.match_detail, name = "match_detail" ),
]
