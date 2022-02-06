from bets.models import BetPoint, TournamentBet


def run():
    # fetch all betpoint and delete them : 
    BetPoint.objects.all().delete()

    # Fetch TournamentBet and set 0 to points_won
    tb = TournamentBet.objects.all()
    for t in tb:
        t.points_won = 0
        t.save()

