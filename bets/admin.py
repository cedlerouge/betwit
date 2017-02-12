from django.contrib import admin
# to edit bettor and auth_user in same admin page
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from models import Bettor, MatchBet, TournamentBet

# Register your models here.

class BettorInline(admin.TabularInline):
    model               = Bettor
    verbose_name_plural = 'bettor'

class UserAdmin(BaseUserAdmin):
    list_display  = ('username', 'first_name', 'last_name', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('first_name', 'last_name',)
    ordering      = ('date_joined',)
    inlines = (BettorInline,)

class BetAdmin(admin.ModelAdmin):
  list_display  = ('player', 'round', 'created_date', 'home_team', 'home_team_score', 'home_team_tries', 'home_team_bonus', 'away_team_bonus', 'away_team_tries', 'away_team_score', 'away_team', 'card', 'drop_goal', 'fight', 'points_won')
  list_filter   = ('player_id',)
  ordering      = ('-created_date',)
  search_fields = ('match', 'player_id',)

  def home_team(self, obj):
    return obj.match_id.home_team_id.name

  def away_team(self, obj):
    return obj.match_id.away_team_id.name

  def player(self, obj):
    return obj.player_id.username

  def round(self, obj):
    return obj.match_id.cup_round

class TournamentAdmin(admin.ModelAdmin):
  list_display = ('tournament_name', 'year', 'player', 'first_team', 'second_team', 'third_team', 'fourth_team', 'fifth_team', 'sixth_team', 'grand_slam', 'wooden_spoon')
  list_filter   = ('player_id',)
  ordering      = ('-created_date', 'player_id')
  search_fields = ('year', 'player_id',)

  def player(self, obj):
    return obj.player_id.username

  def tournament_name(self, obj):
    return obj.tournament_id.name

  def year(self, obj):
    return obj.tournament_id.year

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(MatchBet, BetAdmin)

#admin.site.register(MatchBet)
admin.site.register(TournamentBet, TournamentAdmin)
