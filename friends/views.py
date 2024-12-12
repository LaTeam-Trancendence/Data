from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tables_core.models import Player
from friends.serializers import FriendSerializer
from register.utils import CustomResponse
from django.contrib.auth.models import User

class AddFriendsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        player = Player.objects.get(user=request.user)
        friend_username = request.data.get("friend_username")
        
        try:
            friend = Player.objects.get(user__username=friend_username)
            player.friends.add(friend)
            player.save()
            return CustomResponse.success({
                "message": "ami ajouté avec succes.",
            }, status=200)

        except Player.DoesNotExist:
            return CustomResponse.error({
                "error": "joueur non trouvé"}, status=404)

#pour recuperer la liste d amis d'un joueur connecte
class   FriendListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        player = Player.objects.get(user=request.user)
        friends = player.friends.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)
