from rest_framework import serializers
from .models import User, Player

class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 

    class Meta:
        model = Player
        fields = ['id', 'user', 'language', 'win_pong', 'lose_pong', 'win_tictactoe', 'lose_tictactoe']
