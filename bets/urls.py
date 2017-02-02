from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^u/$', views.UserRedirect.as_view() ),
    url( r'^u/(?P<username>\w+)/$', views.Profile.as_view() ),
    # list tournaments, il only one, display matchbets
    url( r'^$', views.bet_index, name='Index' ),
    url( r'^(?P<tournament_id>[0-9]+)/$', views.tbet_list, name='tbet_list' ),
    url( r'^(?P<tournament_id>[0-9]+)/mbet_list/$', views.mbet_list, name='mbet_list' ),
    url( r'^mbet_add/$', views.matchBet_add ),
    url( r'^mbet/(?P<mbet_id>[0-9]+)/$', views.mbet_detail, name="mbet_detail" ),
    url( r'^tbet_add/$', views.tournamentBet_add, name="tbet_add" ),
    url( r'^tbet/(?P<tbet_id>[0-9]+)/$', views.tbet_detail, name='tbet_detail' ),
    
    
    
]
