from django.shortcuts import render
from django.http import JsonResponse
from tables_core.models import CustomUser, Player, Match
from django.contrib.auth.models import User
from register.utils import CustomResponse
from stats.serializers import PlayerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# \\_________________________________________//


class statsPlayerView(APIView):
    
    # \\_______recupere les stats____________//
    
    def get(self, request, *args, **kwargs):
        
        player_id = kwargs.get('player_id', None)

        if player_id: 
            try:
                player = Player.objects.get(id=player_id)
                serializer = PlayerSerializer(player)
                return CustomResponse.success(
                    data={"player": serializer.data},
                    message="Statistiques joueur ok",
                    status_code=200
                )
            except Player.DoesNotExist:
                return CustomResponse.error(
                    errors={"player_id": "Joueur non trouvé."},
                    message="Erreur : le joueur n'existe pas.",
                    status_code=404)
                
        else: 
            players = Player.objects.all()
            serializer = PlayerSerializer(players, many=True)
            return CustomResponse.success(
                data={"players": serializer.data},
                message="Statistiques tous les joueurs ok",
                status_code=200
            )
        
        # \\_______modifie les stats____________//
        
    def put(self, request, *args, **kwargs):
        
        player_id = kwargs.get('player_id', None)
        
        if not player_id:
            return CustomResponse.error(
                errors={"player_id": "ID du joueur requis."},
                message="Erreur : aucun ID fourni.",
                status_code=400
            )

        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return CustomResponse.error(
                errors={"player_id": "Joueur non trouvé."},
                message="Erreur : le joueur n'existe pas.",
                status_code=404
            )

        serializer = PlayerSerializer(player, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data={"player": serializer.data},
                message="Statistiques mises à jour avec succès.",
                status_code=200
            )
        return CustomResponse.error(
            errors=serializer.errors,
            message="Erreur lors de la mise à jour des statistiques.",
            status_code=400
        )
