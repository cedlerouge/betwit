from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^u/$', views.UserRedirect.as_view(), name='profile'),
    url( r'^u/(?P<username>\w+)/$', views.UserProfile.as_view()),
    # list tournaments, il only one, display matchbets
    url( r'^$', views.bet_index, name='index' ),
    url( r'^mybets/$', views.MyBets.as_view(), name='mybets'),
    url( r'^tbet_add/$', views.bet_index, name="tbet_add" ),
    url( r'^tbet_add/(?P<tournament_id>[0-9]+)/$', views.tournamentBet_add, name="tbet_add" ),
    url( r'^tbet_add/(?P<tournament_id>[0-9]+)/(?P<tbet_id>[0-9]+)/$', views.tournamentBet_add, name="tbet_add" ),
    url( r'^tbet/(?P<tbet_id>[0-9]+)/$', views.tbet_detail, name='tbet_detail' ),
    url( r'^(?P<tournament_id>[0-9]+)/$', views.tbet_list, name='tbet_list' ),
    url( r'^(?P<tournament_id>[0-9]+)/mbet_list/$', views.mbet_available, name='mbet_list' ),
    url( r'^mbet_add/$', views.matchBet_add, name='mbet_add' ),
    url( r'^mbet_add/(?P<tournament_id>[0-9]+)/$', views.matchBet_add, name='mbet_add' ),
    url( r'^mbet_add/(?P<tournament_id>[0-9]+)/(?P<mbet_id>[0-9]+)/$', views.matchBet_add, name='mbet_add' ),
    url( r'^mbet_add/(?P<tournament_id>[0-9]+)/match/(?P<m_id>[0-9]+)/$', views.matchBet_add, name='mbet_add_mid' ),
    url( r'^mbet/(?P<mbet_id>[0-9]+)/$', views.mbet_detail, name="mbet_detail" ),
    url( r'^prognosis/$', views.prognosis, name="prognosis" ),
    url( r'^rank/$', views.BetRanking.as_view(), name="betrank" ),

]
