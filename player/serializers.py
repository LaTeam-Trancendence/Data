from rest_framework import serializers
from tables_core.models import CustomUser, Player, Match
from register.serializers import UserSerializer


# \\ _______________________________________________//


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 

    class Meta:
        model = Player
        fields = ['id', 'user', 'language', 'win_pong', 'lose_pong',
                  'win_tictactoe', 'lose_tictactoe']