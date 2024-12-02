from django.contrib import admin
from tables_core.models import CustomUser, Player, Match
# Register your models here.

@admin.register(CustomUser)
class CustomUser_admin(admin.ModelAdmin):
    list_display = ["username", "id"]
    pass

@admin.register(Player)
class Player_admin(admin.ModelAdmin):
    list_display = ['id', 'user', 'language', 'win_pong', 'lose_pong', 'win_tictactoe', 'lose_tictactoe']
    pass

@admin.register(Match)
class Match_admin(admin.ModelAdmin):
    list_display = ['id', 'user', 'adv', 'user_score', 'adv_score', 
                    'result', 'date', 'start_match', 'end_match']
    
    exclude = ['duration']
    
    pass