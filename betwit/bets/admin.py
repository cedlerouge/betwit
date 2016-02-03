from django.contrib import admin

class BetAdmin(admin.ModelAdmin):
  list_display 	= ('user', 'match', 'created_date', 'scoreA', 'scoreB')
  list_filter  	= ('user',)
  ordering	= ('-created_date',)
  search_fields	= ('match',)
# Register your models here.

from models import Bet

admin.site.register(Bet, BetAdmin)

