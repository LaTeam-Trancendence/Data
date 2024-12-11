from django.shortcuts import render
from django.http import JsonResponse
from tables_core.models import CustomUser, Player, Match
from django.contrib.auth.models import User
from register.utils import CustomResponse
from stats.serializers import MatchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def up_player_stats(match):
    user = match.user
    adv = match.adv
    
    
    if match.result == 1:
        user.total_win += 1
        user.total_lose += 1
    elif match.result == 2:
        adv.total_win += 1
        adv.total_lose += 1
        
    user.save()
    adv.save()
    
    # A voir pour ranking (placer avant save)
    # user.total_matches += 1
    # adv.total_matches += 1
    # user_score += match.player_score
    # adv_score += match.adv_score


class FinalizeMatchView(APIView):
    
    # \\_______recupere les stats____________//
    
    def get(self, request, *args, **kwargs):
        
        username = request.query_params.get("username", None)
        # si recherche par id match_id = kwargs.get('match_id', None) 
        # ajoute un if - matches = Match.objects.filter(id= match_id).filter() 
        
        if username:
            try:
                player = Player.objects.get(username=username)
                matches = Match.objects.filter(user=player)
                serializer = MatchSerializer(matches, many=True)
                return CustomResponse.success(
                    data={"matches": serializer.data},
                    message=f"Matches pour le joueur {username}.",
                    status_code=200
                )
            except Player.DoesNotExist:
                return CustomResponse.error(
                    {"error": f"Joueur avec username '{username}' introuvable."},
                    status_code=404
                )
        else:
            matches = Match.objects.all()
            serializer = MatchSerializer(matches, many=True)
            return CustomResponse.success(
                data={"matches": serializer.data},
                message="Statistiques de tous les matchs récupérées.",
                status_code=200
            )    
            
        # \\_______modifie les stats____________//
            
    def post(self, request, *args, **kwargs):
        
        match_id = request.data.get("match_id")
        user_score = request.data.get("user_score")
        adv_score = request.data.get("adv_score")

        if match_id:
            try:
                match = Match.objects.get(id=match_id)
                match.user_score = user_score
                match.adv_score = adv_score
                if user_score > adv_score:
                    match.result = 1
                elif user_score < adv_score:
                    match.result = 2 
                match.save()

                up_player_stats(match)

                return CustomResponse.success({
                    "message": "Match finalisé, statistiques mises à jour.",
                    }, status=200)
            except Match.DoesNotExist:
                return CustomResponse.error({
                    "error": "Match introuvable.",
                    }, status=400)
        else:
            match = Match.objects.all()
            serializer = MatchSerializer(match, many=True)
            return CustomResponse.success(
                data={"Match": serializer.data},
                message="Statistiques tous les mqtchs ok",
                status_code=200
            )