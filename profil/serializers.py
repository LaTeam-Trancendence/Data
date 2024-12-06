from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tables_core.models import CustomUser, Player, Match
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password 
from Back import settings
from player.serializers import PlayerSerializer

class DisplayPlayerSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'player']

    def get_player(self, obj):
        try:
            player = Player.objects.get(user=obj)
            return PlayerSerializer(player).data
        except Player.DoesNotExist:
            return None
        
        
class CustomPlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    image = serializers.ImageField(source='user.image')
    class Meta:
        model = Player
        fields = ['id', 'username', 'password', 'image', 'friends',
                  'win_pong', 'lose_pong', 'win_tictactoe', 'lose_tictactoe']

class ListPlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = Player
        fields = ['username']
        