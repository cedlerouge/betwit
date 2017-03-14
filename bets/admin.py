from django.contrib import admin
# to edit bettor and auth_user in same admin page
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import Profile, MatchBet, TournamentBet

# Register your models here.

class ProfileInline(admin.StackedInline): #TabularInline):
    model               = Profile
    can_delete          = False
    verbose_name_plural = 'Profile'
    fk_name             = 'user'

class CustomUserAdmin(UserAdmin):
    inlines     = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
    #list_display  = ('username', 'first_name', 'last_name', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
    #search_fields = ('first_name', 'last_name',)
    #ordering      = ('date_joined',)
    #inlines = (UserProfileInline,)

class BetAdmin(admin.ModelAdmin):
  list_display  = ('player', 'round', 'created_date', 'home_team', 'home_team_score', 'home_team_tries', 'home_team_bonus', 'away_team_bonus', 'away_team_tries', 'away_team_score', 'away_team', 'card', 'drop_goal', 'fight', 'points_won')
  list_filter   = ('player',)
  ordering      = ('-created_date',)
  search_fields = ('match', 'player',)

  def home_team(self, obj):
    return obj.match.home_team.name

  def away_team(self, obj):
    return obj.match.away_team.name

  def player(self, obj):
    return obj.player.username

  def round(self, obj):
    return obj.match.cup_round

class TournamentAdmin(admin.ModelAdmin):
  list_display = ('tournament_name', 'year', 'player', 'first_team', 'second_team', 'third_team', 'fourth_team', 'fifth_team', 'sixth_team', 'grand_slam', 'wooden_spoon')
  list_filter   = ('player',)
  ordering      = ('-created_date', 'player')
  search_fields = ('year', 'player',)

  def player(self, obj):
    return obj.player.username

  def tournament_name(self, obj):
    return obj.tournament.name

  def year(self, obj):
    return obj.tournament.year

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(MatchBet, BetAdmin)

#admin.site.register(MatchBet)
admin.site.register(TournamentBet, TournamentAdmin)
