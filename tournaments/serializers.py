from rest_framework import serializers
from .models import Team, Tournament, Match, TeamStat


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "nationality", "logo", "flag"]


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ["id", "name", "year", "begins", "state"]


class MatchSerializer(serializers.ModelSerializer):
    home_team = serializers.StringRelatedField()
    away_team = serializers.StringRelatedField()
    tournament = serializers.StringRelatedField()

    class Meta:
        model = Match
        fields = [
            "id",
            "tournament",
            "date",
            "cup_round",
            "home_team",
            "home_team_score",
            "home_team_tries",
            "home_team_bonus",
            "away_team",
            "away_team_score",
            "away_team_tries",
            "away_team_bonus",
            "card",
            "drop_goal",
            "fight",
            "odds",
            "jokerbet_text",
            "jokerbet_response",
            "jokerbet_win_pts",
            "jokerbet_lose_pts",
        ]


class TeamStatSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = TeamStat
        fields = [
            'id',
            'team',
            'tournament',
            'played',
            'win',
            'draw',
            'lose',
            'ptsfor',
            'ptsagainst',
            'ptsdiff',
            'tryfor',
            'tryagainst',
            'trybonus',
            'losebonus',
            'points',
        ]


class MatchDetailSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = Match
        fields = [
            "id",
            "tournament",
            "date",
            "cup_round",
            "home_team",
            "home_team_score",
            "home_team_tries",
            "home_team_bonus",
            "away_team",
            "away_team_score",
            "away_team_tries",
            "away_team_bonus",
            "card",
            "drop_goal",
            "fight",
            "odds",
            "jokerbet_text",
            "jokerbet_response",
            "jokerbet_win_pts",
            "jokerbet_lose_pts",
            "created_date",
            "modified_date",
        ]
