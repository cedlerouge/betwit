from django.contrib import admin
from models import Tournament, Team, Match, MatchPoint, TeamMatchPoint, TeamStat
# Register your models here.

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(MatchPoint)
admin.site.register(TeamMatchPoint)
admin.site.register(TeamStat)
