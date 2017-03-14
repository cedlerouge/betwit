from django.contrib import admin
from models import Tournament, Team, Match, MatchPoint, TeamMatchPoints, TeamStat
# Register your models here.

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(MatchPoint)
admin.site.register(TeamMatchPoints)
admin.site.register(TeamStat)
