from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from register.utils import CustomResponse
from register.serializers import UserSerializer , LoginSerializer, DeleteSerializer
from Back import settings
import logging
import os


# \\_________________register___________________________________//


logger = logging.getLogger(__name__)

class RegisterUserView(APIView):
    print('image')
    permission_classes = [AllowAny] 
    
    # def get(self, request, *args, **kwargs):    #test request Get
    #      return CustomResponse.success({
    #         "status": "success",
    #         "message": "Veuillez envoyer une requête POST pour vous inscrire.",
    #     }, status_code=200)
    
    def post(self, request, *args, **kwargs):
        data=request.data
        serializer = UserSerializer(data=request.data)
        print(data)
        if serializer.is_valid():
            user = serializer.save()
            return(CustomResponse.success(
                {"CustomUser": "create"},
                status_code=201
            ))
        return(CustomResponse.error(
            {"error": serializer.errors},
            status_code=400
        ))
    

# \\ ___________________login___________________________________//


class LoginView(APIView):
    permission_classes = [AllowAny]
      
    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return(CustomResponse.success(
                    {"CustomUser": "success login"},
                    status_code=200
            ))
            else:
                return(CustomResponse.error(
                {"error": "champ vide"},
                status_code=400
        ))
        else:
            return(CustomResponse.error(
                {"error": "le pseudo ou le mdp n'est pas valide"},
                status_code=401
        ))
            
            
 # \\___________________logout________________________//
 
 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):

        if request.user.is_authenticated:
            logout(request)
            return CustomResponse.success(
                {"message": "Déconnexion réussie."},
                status_code=200
            )
        else:
            return CustomResponse.error(
                {"error": "Aucune session active."},
                status_code=400
            )
        
 # \\_________________Anonim/delete________________________//
 
 
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        
        if user:
            anoCustomUser(user),         
            return CustomResponse.success(
            {"message": "Objet supprimé avec succès."},
            status_code=200)
        return(CustomResponse.error(
                {"errors": anoCustomUser.errors},
                status_code=400
        ))
        
def anoCustomUser(user):


    if user.image:
        image_path = os.path.join(settings.MEDIA_ROOT, user.image.name)

    if os.path.isfile(image_path):
            os.remove(image_path)
    
    user.username = f"user_{user.id}"
    user.image = 'player_picture/default_avatar.png'
    user.is_anonymized = True
    user.save()
    
 # \\___________Healthcheck pour docker________________//       
     
            
class HealthCheckView(APIView):
    
    def get(self, request):
        return (CustomResponse.success(
            {"status": "ok"},
            status_code=200
        ))
            
            
            
# class DeleteAccountView(APIView):
    
#     def delete(self, request, *args, **kwargs):
        
#         user = request.user
#         if user.is_authenticated:
#             anonymize_and_delete_user(user)
#             return Response({"message": "Votre compte a été supprimé et anonymisé."}, status=200)
#         return Response({"error": "Utilisateur non authentifié."}, status=401)