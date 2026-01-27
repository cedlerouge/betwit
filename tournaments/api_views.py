from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from .models import Team, Tournament, Match, TeamStat
from .serializers import (
    TeamSerializer,
    TournamentSerializer,
    MatchSerializer,
    MatchDetailSerializer,
    TeamStatSerializer,
)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all().order_by("name")
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]


class TournamentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tournament.objects.all().order_by("-year")
    serializer_class = TournamentSerializer
    permission_classes = [permissions.AllowAny]


class MatchFilter(filters.FilterSet):
    tournament = filters.NumberFilter(field_name='tournament__id')
    date_from = filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='date', lookup_expr='lte')
    upcoming = filters.BooleanFilter(method='filter_upcoming')
    home_team = filters.NumberFilter(field_name='home_team__id')
    away_team = filters.NumberFilter(field_name='away_team__id')

    class Meta:
        model = Match
        fields = ['tournament', 'cup_round', 'date_from', 'date_to', 'home_team', 'away_team']

    def filter_upcoming(self, queryset, name, value):
        from django.utils import timezone
        if value:
            return queryset.filter(date__gte=timezone.now())
        return queryset


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.select_related("home_team", "away_team", "tournament").all().order_by("date")
    serializer_class = MatchSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = MatchFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MatchDetailSerializer
        return MatchSerializer


class TeamStatFilter(filters.FilterSet):
    tournament = filters.NumberFilter(field_name='tournament__id')

    class Meta:
        model = TeamStat
        fields = ['tournament']


class TeamStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamStat.objects.select_related("team", "tournament").all().order_by("-points", "-ptsdiff")
    serializer_class = TeamStatSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = TeamStatFilter
