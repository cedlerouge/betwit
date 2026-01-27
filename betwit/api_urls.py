from django.urls import path, include
from rest_framework import routers
from tournaments.api_views import TeamViewSet, TournamentViewSet, MatchViewSet, TeamStatViewSet
from bets.api_views import (
    MatchBetViewSet,
    BetPointViewSet,
    MatchRatingViewSet,
    TournamentBetViewSet,
    ProfileViewSet,
    UserRankingViewSet,
)
from .api_views import HomeDataAPIView

router = routers.DefaultRouter()
# tournaments
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'tournaments', TournamentViewSet, basename='tournament')
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'teamstats', TeamStatViewSet, basename='teamstat')
# bets
router.register(r'matchbets', MatchBetViewSet, basename='matchbet')
router.register(r'tournamentbets', TournamentBetViewSet, basename='tournamentbet')
router.register(r'betpoints', BetPointViewSet, basename='betpoint')
router.register(r'ratings', MatchRatingViewSet, basename='rating')
router.register(r'rankings', UserRankingViewSet, basename='ranking')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('accounts.urls')),  # JWT auth endpoints
    path('auth/session/', include('rest_framework.urls')),  # session login/logout for browsable API
    path('home/', HomeDataAPIView.as_view(), name='home-data'),
]
