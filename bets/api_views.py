from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from .models import MatchBet, BetPoint, MatchRating, Profile, TournamentBet
from .serializers import (
    MatchBetSerializer,
    BetPointSerializer,
    MatchRatingSerializer,
    ProfileSerializer,
    TournamentBetSerializer,
    UserRankingSerializer,
)


class MatchBetViewSet(viewsets.ModelViewSet):
    serializer_class = MatchBetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own bets
        return MatchBet.objects.filter(player=self.request.user).order_by("-created_date")

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)


class BetPointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BetPoint.objects.all().order_by("-points_won")
    serializer_class = BetPointSerializer
    permission_classes = [permissions.AllowAny]


class MatchRatingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MatchRating.objects.all().order_by("-date")
    serializer_class = MatchRatingSerializer
    permission_classes = [permissions.AllowAny]


class TournamentBetViewSet(viewsets.ModelViewSet):
    serializer_class = TournamentBetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TournamentBet.objects.filter(player=self.request.user).order_by("-created_date")

    def perform_create(self, serializer):
        serializer.save(player=self.request.user)


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRankingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        rankings = (
            BetPoint.objects
            .values('player__id', 'player__username')
            .annotate(
                total_points=Sum('points_won'),
                matches_bet=Count('id')
            )
            .order_by('-total_points')
        )

        result = []
        for rank, item in enumerate(rankings, start=1):
            result.append({
                'rank': rank,
                'user_id': item['player__id'],
                'username': item['player__username'],
                'total_points': item['total_points'] or 0,
                'matches_bet': item['matches_bet'],
            })

        serializer = UserRankingSerializer(result, many=True)
        return Response(serializer.data)
