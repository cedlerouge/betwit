from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import MatchBet, BetPoint, MatchRating, Profile, TournamentBet
from tournaments.models import Tournament, Team


class MatchBetSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MatchBet
        fields = [
            "id",
            "player",
            "match",
            "home_team_score",
            "home_team_tries",
            "home_team_bonus",
            "away_team_score",
            "away_team_tries",
            "away_team_bonus",
            "card",
            "drop_goal",
            "fight",
            "jokerbet_text",
            "jokerbet_value",
            "points_won",
            "created_date",
            "modified_date",
        ]
        read_only_fields = ["points_won", "created_date", "modified_date"]


class BetPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetPoint
        fields = ["id", "player", "match", "matchbet", "points_won"]


class MatchRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRating
        fields = [
            "id",
            "match",
            "ht_votes",
            "at_votes",
            "null_votes",
            "total_votes",
            "ht_rating",
            "at_rating",
            "null_rating",
            "date",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    total_points = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'is_admin', 'tz', 'points_won', 'total_points', 'language']
        read_only_fields = ['id', 'is_admin', 'points_won']

    def get_total_points(self, obj):
        return BetPoint.objects.filter(player=obj.user).aggregate(
            total=Sum('points_won')
        )['total'] or 0

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.email = user_data.get('email', user.email)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()

        instance.tz = validated_data.get('tz', instance.tz)
        instance.language = validated_data.get('language', instance.language)
        instance.save()
        return instance


class TournamentBetSerializer(serializers.ModelSerializer):
    player = serializers.StringRelatedField(read_only=True)
    tournament_name = serializers.CharField(source='tournament.__str__', read_only=True)
    first_team_name = serializers.CharField(source='first_team.name', read_only=True)
    second_team_name = serializers.CharField(source='second_team.name', read_only=True)
    third_team_name = serializers.CharField(source='third_team.name', read_only=True)
    fourth_team_name = serializers.CharField(source='fourth_team.name', read_only=True)
    fifth_team_name = serializers.CharField(source='fifth_team.name', read_only=True)
    sixth_team_name = serializers.CharField(source='sixth_team.name', read_only=True)

    class Meta:
        model = TournamentBet
        fields = [
            'id',
            'player',
            'tournament',
            'tournament_name',
            'first_team',
            'first_team_name',
            'second_team',
            'second_team_name',
            'third_team',
            'third_team_name',
            'fourth_team',
            'fourth_team_name',
            'fifth_team',
            'fifth_team_name',
            'sixth_team',
            'sixth_team_name',
            'grand_slam',
            'wooden_spoon',
            'points_won',
            'created_date',
            'modified_date',
        ]
        read_only_fields = ['points_won', 'created_date', 'modified_date']


class UserRankingSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    total_points = serializers.FloatField()
    matches_bet = serializers.IntegerField()
