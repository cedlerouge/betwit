from django.contrib import admin

class BetAdmin(admin.ModelAdmin):
  list_display 	= ('user', 'round', 'teamA', 'teamB', 'created_date', 'scoreA', 'scoreB', 'triesA', 'triesB', 'card', 'drop_goal', 'fight', 'points_won')
  list_filter  	= ('user',)
  ordering	= ('-created_date',)
  search_fields	= ('match',)

  def teamA(self, obj):
    return obj.match.teamA

  def teamB(self, obj):
    return obj.match.teamB

  def round(self, obj):
    return obj.match.cup_round

# Register your models here.

from models import Bet, BetCup

admin.site.register(Bet, BetAdmin)
admin.site.register(BetCup)
