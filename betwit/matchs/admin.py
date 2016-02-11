from django.contrib import admin

class MatchAdmin(admin.ModelAdmin):
  list_display	= ('teamA', 'teamB', 'match_date', 'cup_round', 'scoreA', 'scoreB', 'triesA', 'triesB', 'card', 'drop_goal', 'fight')
  list_filter   = ('teamA', 'cup_round',)
  ordering      = ('match_date',)
  search_fields = ('teamA',)

# Register your models here.

from models import Match

admin.site.register(Match, MatchAdmin)
