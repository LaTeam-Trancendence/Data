from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from register.utils import CustomResponse
from register.serializers import UserSerializer , LoginSerializer
from Back import settings


# \\_________________register___________________________________//


class RegisterUserView(APIView):
    permission_classes = [AllowAny] 
    
    def get(self, request, *args, **kwargs):    #test request Get
        return CustomResponse.success({
            "status": "success",
            "message": "Veuillez envoyer une requête POST pour vous inscrire.",
        }, status_code=200)
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return(CustomResponse.success(
                data = {"CustomUser": UserSerializer(user).Meta},
                message="succes",
                status_code=201
            ))
        return(CustomResponse.error(
            errors=serializer.errors,
            message="error",
            status_code=400
        ))

# \\ ___________________login___________________________________//

class LoginView(APIView):
      
    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return(CustomResponse.succes(
                    data = {"CustomUser": UserSerializer(user).Meta},
                    message="succes",
                    status_code=200
            ))
            else:
                return(CustomResponse.error(
                    errors=serializer.errors,
                    message="error",
                    status_code=400
        ))
        else:
            return(CustomResponse.error(
                errors=serializer.errors,
                message="error",
                status_code=401
        ))

def anoCustomUser(user):
    
    user.username = f"user_{user.id}"
    user.image = None 
    user.save()
    
class DeleteAccountView(APIView):
    
    def post(self, request, *args, **kwargs):

        user = request.user
        
        if user:
            anoCustomUser(user)
            return(CustomResponse.succes(
                data = {"CustomUser": UserSerializer(user).Meta},
                message="anonimisation reussie",
                status_code=200
            ))
        else:
            return(CustomResponse.error(
                errors=anoCustomUser.errors,
                message="error",
                status_code=400
        ))
            
            
            
            
            
            
            
# class DeleteAccountView(APIView):
    
#     def delete(self, request, *args, **kwargs):
        
#         user = request.user
#         if user.is_authenticated:
#             anonymize_and_delete_user(user)
#             return Response({"message": "Votre compte a été supprimé et anonymisé."}, status=200)
#         return Response({"error": "Utilisateur non authentifié."}, status=401)