from rest_framework import serializers
from tables_core.models import CustomUser, Player, Match
from register.serializers import UserSerializer


# \\ _______________________________________________//


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 

    class Meta:
        model = Player
        fields = ['id', 'user', 'friends', 'language', 'win_pong', 'lose_pong',
                  'win_tictactoe', 'lose_tictactoe']
   
    def create(self, validated_data):

        if 'user' not in validated_data:
            raise serializers.ValidationError({"user": "Un utilisateur doit être spécifié."})
        return super().create(validated_data)
    
