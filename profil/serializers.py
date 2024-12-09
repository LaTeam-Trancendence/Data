from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tables_core.models import CustomUser, Player, Match
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password 
from Back import settings
from player.serializers import PlayerSerializer


class FriendSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = Player
        fields = ['username', 'status']
        
        
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
    friends = FriendSerializer(many=True)
    
    class Meta:
        model = Player
        fields = ['id', 'username', 'password', 'image', 'friends', 'status',
                  'win_pong', 'lose_pong', 'win_tictactoe', 'lose_tictactoe']

class ListPlayerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = Player
        fields = ['username', 'friends', 'status', 'win_pong', 'lose_pong', 'win_tictactoe', 'lose_tictactoe']
        
        
# class PlayerImageUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['image'] #inclu uniquement le champ image


#     def update(self, instance, validated_data):
#         instance.image = validated_data.get("image", instance.image)
#         instance.save()
#         return instance