from django.shortcuts import render
from django.http import JsonResponse
from tables_core.models import CustomUser, Player, Match
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from register.utils import CustomResponse
from .serializers import DisplayPlayerSerializer, CustomPlayerSerializer
from Back import settings
import logging


# class DisplayPlayerView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#             user = request.user
#             serializer = DisplayPlayerSerializer(user)
#             return(CustomResponse.success(
#                 serializer.data,
#                 status_code=200
#             ))
            
class DisplayPlayerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            player = Player.objects.get(user=request.user)
            serializer = CustomPlayerSerializer(player)
            return(CustomResponse.success(
                serializer.data,
                status_code=200
            ))