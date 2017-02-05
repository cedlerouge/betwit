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

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(MatchBet)
admin.site.register(TournamentBet)
