from django.urls import path, re_path
from . import views, views_stats

app_name = 'bets'

urlpatterns = [
    path('u/', views.UserRedirect.as_view(), name='profile'),
    re_path(r'^u/(?P<username>\w+)/$', views.UserProfile.as_view()),
    path('', views.mbet_available, name='mbet_list'),
    path('mybets/', views.MyBets.as_view(), name='mybets'),
    path('tbet_add/', views.bet_index, name='tbet_add'),
    re_path(r'^tbet_add/(?P<tournament_id>[0-9]+)/$', views.tournamentBet_add, name='tbet_add'),
    re_path(r'^tbet_add/(?P<tournament_id>[0-9]+)/(?P<tbet_id>[0-9]+)/$', views.tournamentBet_add, name='tbet_add'),
    re_path(r'^tbet/(?P<tbet_id>[0-9]+)/$', views.tbet_detail, name='tbet_detail'),
    re_path(r'^(?P<tournament_id>[0-9]+)/$', views.tbet_list, name='tbet_list'),
    re_path(r'^(?P<tournament_id>[0-9]+)/mbet_list/$', views.mbet_available, name='mbet_list'),
    re_path(r'^mbet_add/(?P<tournament_id>[0-9]+)/$', views.matchBet_add, name='mbet_add'),
    re_path(r'^mbet_add/(?P<tournament_id>[0-9]+)/(?P<mbet_id>[0-9]+)/$', views.matchBet_add, name='mbet_add_post_mid'),
    re_path(r'^mbet_add/(?P<tournament_id>[0-9]+)/match/(?P<m_id>[0-9]+)/$', views.matchBet_add, name='mbet_add_mid'),
    re_path(r'^mbet/(?P<mbet_id>[0-9]+)/$', views.mbet_detail, name='mbet_detail'),
    path('prognosis/', views.prognosis, name='prognosis'),
    path('stats/', views_stats.stats, name='stats'),
    path('stats-perso/', views_stats.stats_perso, name='stats_perso'),
    path('rank/', views.BetRanking.as_view(), name='betrank'),
]
