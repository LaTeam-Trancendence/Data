from rest_framework import serializers
from tables_core.models import CustomUser, Player


class FriendSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = Player
        fields = ['username', 'status']