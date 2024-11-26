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

