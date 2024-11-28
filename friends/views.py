from django.shortcuts import render
from rest_framework.views import APIView
from rest_frameword.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Player
from .serializers import PlayerSerializer, FriendSerializer
from register.utils import CustomResponse
from django.contrib.auth.models import User

class AddFriendsView(APIView):
    
    #acces au joueur authentifier
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        player = Player.objects.get(user=request.user)
        friend_id = request.data.get("friend_id")
        
        try:
            friend = Player.objects.get(id=friend_id)
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
