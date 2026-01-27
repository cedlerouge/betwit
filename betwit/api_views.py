from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.db.models import Sum, Count

from tournaments.models import Match, TeamStat, Tournament
from tournaments.serializers import MatchSerializer, TeamStatSerializer
from bets.models import BetPoint, MatchRating


class HomeDataAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get the current active tournament
        active_tournament = Tournament.objects.filter(state='1').first()

        # Top 5 players (user rankings)
        top_players = (
            BetPoint.objects
            .values('player__id', 'player__username')
            .annotate(
                total_points=Sum('points_won'),
                matches_bet=Count('id')
            )
            .order_by('-total_points')[:5]
        )

        top_players_data = []
        for rank, item in enumerate(top_players, start=1):
            top_players_data.append({
                'rank': rank,
                'user_id': item['player__id'],
                'username': item['player__username'],
                'total_points': item['total_points'] or 0,
                'matches_bet': item['matches_bet'],
            })

        # Next 3 matches with ratings
        now = timezone.now()
        upcoming_matches = Match.objects.select_related(
            'home_team', 'away_team', 'tournament'
        ).filter(date__gte=now).order_by('date')[:3]

        matches_data = []
        for match in upcoming_matches:
            match_data = MatchSerializer(match).data
            # Get the latest rating for this match
            latest_rating = MatchRating.objects.filter(match=match).order_by('-date').first()
            if latest_rating:
                match_data['rating'] = {
                    'ht_rating': latest_rating.ht_rating,
                    'at_rating': latest_rating.at_rating,
                    'null_rating': latest_rating.null_rating,
                    'total_votes': latest_rating.total_votes,
                }
            else:
                match_data['rating'] = None
            matches_data.append(match_data)

        # Team standings for active tournament
        standings_data = []
        if active_tournament:
            standings = TeamStat.objects.select_related('team', 'tournament').filter(
                tournament=active_tournament
            ).order_by('-points', '-ptsdiff')

            standings_data = TeamStatSerializer(standings, many=True).data

        return Response({
            'top_players': top_players_data,
            'upcoming_matches': matches_data,
            'standings': standings_data,
            'active_tournament': {
                'id': active_tournament.id,
                'name': str(active_tournament),
            } if active_tournament else None,
        })
