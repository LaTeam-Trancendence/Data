from django.contrib import admin
from tables_core.models import CustomUser, Player, Match


#@admin.stats(Match)
# class stats_admin(admin.ModelAdmin):
#     list_display = ['id', 'user','user_score', 'adv', 'adv_score', 'result',
#                   'date', 'duration']
#     pass
