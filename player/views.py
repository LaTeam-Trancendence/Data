from django.shortcuts import render
from django.http import JsonResponse
from tables_core.models import CustomUser, Player, Match
from django.contrib.auth.models import User
from register.utils import CustomResponse
from player.serializers import PlayerSerializer, PlayerStatSerializer, StatUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from PIL import Image

# \\_________________________________________//

class statsPlayerView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return(CustomResponse.success(
                {"stats": "ok"},
                status_code=201
            ))
        return(CustomResponse.error(
            {"errors": serializer.errors},
            status_code=400
        ))

    # \\_______recupere les stats____________//

    def get(self, request, *args, **kwargs):

        player_id = kwargs.get('player_id', None)

        if player_id:
            try:
                player = Player.objects.get(id=player_id)
                serializer = PlayerSerializer(player)
                return(CustomResponse.success(
                {"stats joueurs": "ok"},
                status_code=201
            ))
            except Player.DoesNotExist:
                return(CustomResponse.error(
                {"errors": "joueur non trouve"},
                status_code=404
            ))

        else:
            #players = Player.objects.filter(status=True)
            players = Player.objects.all()
            serializer = PlayerSerializer(players, many=True)
            return(CustomResponse.success(
                {"stats joueurs": "stats de tous les joueurs ok"},
                status_code=200
            ))

    # \\_______________modifie les stats____________//

# attention au customResponse

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

# mise a jour des statistiques
class   PlayerStatAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request): # stat_type = "victoire pong" ou "defaite"
        try:
            serializer = StatUpdateSerializer(data=request.data)
            if not serializer.is_valid():
                return CustomResponse.error(
                errors=serializer.errors, 
                status_code=400
            )
            player = Player.objects.get(user=request.user)
            stat_type = serializer.validated_data["stat_type"]
            if stat_type == "win_pong":
                player.win_pong += 1
            elif stat_type == "lose_pong":
                player.lose_pong += 1
            elif stat_type == "win_tictactoe":
                player.win_tictactoe += 1
            elif stat_type == "lose_tictactoe":
                player.lose_tictactoe += 1
            else:
                return CustomResponse.error(
                    errors={"error": "Invalid stat type"},
                    status_code=400)
            
            player.save()
            return CustomResponse.success(
                {"message": "stat updated"},
                status_code=200)
        except Player.DoesNotExist:
            return CustomResponse.error({"error": "Player not found"},
                            status_code=404)

class PlayerDetailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            player = Player.objects.get(user=request.user)
            serializer = PlayerStatSerializer(player)
            return CustomResponse.success(serializer.data, status_code=200)
        except Player.DoesNotExist:
            return CustomResponse.error({"error": "Player not found"},
                                  status_code=404)
                
''''
class   signupAPIView(APIView):
    serializer_class = PlayerSerializer
    permission_classes = [AllowAny]
    
# \\________________verfier les reponses___________//

class   changeImageAPIView(APIView):
    permission_classes =[IsAuthenticated,]
    parser_classes = [FormParser, MultiPartParser,]

    def post(self, request, format=None):
        user = request.user
        serializer = PlayerImageUploadSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        else:
            return Response(data=serializer.errors, status=500)
'''
''''
class UploadPlayerImageView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Pour accepter les fichiers

    def post(self, request):
        user = request.user  # Récupère l'utilisateur connecté

        image = request.FILES.get('image')
        if not image:
            return Response({"error": "Aucune image n'a été envoyée."}, status=400)

        # Valider la taille de l'image
        try:
            img = Image.open(image)
            if img.height > 400 or img.width > 400:
                return Response({"error": "Les dimensions de l'image doivent être de 400x400 pixels maximum."}, status=400)
        except Exception as e:
            return Response({"error": f"Erreur lors de la validation de l'image : {e}"}, status=400)

        # Sauvegarder l'image
        user.image = image
        user.save()

        return Response({"message": "Image mise à jour avec succès", "image_url": user.image.url}, status=200)
'''

''''
    def post(self, request):
        user = request.user  # Récupère l'utilisateur connecté
        serializer = PlayerImageUploadSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Image mise à jour avec succès", "image_url": user.image.url}, status=200)

        return Response(serializer.errors, status=400)
'''
# class PlayerCreateView(APIView):
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         if not user.is_authenticated:
#             return Response(
#                 {"Authentification requise pour créer un joueur."},
#                 status=401)

#         data = request.data.copy()
#         data['user'] = user.id
#         serializer = PlayerSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

#     def get(self, request):
#         players = Player.objects.all()
#         print(players)
#         serializer = PlayerSerializer(players, many=True)
#         return Response(serializer.data)

# class DisplayPlayerView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#             player = Player.objects.get(user=request.user)
#             serializer = DisplayPlayerSerializer(player)
#             return(CustomResponse.success(
#                 serializer.data,
#                 status_code=200
#             ))
#         # return Response({"error": "Joueur introuvable."}, status=404)


