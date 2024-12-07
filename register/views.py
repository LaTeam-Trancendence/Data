from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from register.utils import CustomResponse
from register.serializers import UserSerializer , LoginSerializer, DeleteSerializer
from Back import settings
import logging
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import PlayerImageUploadSerializer
from PIL import Image
from rest_framework.response import Response


# \\_________________register___________________________________//

logger = logging.getLogger(__name__)

class RegisterUserView(APIView):
    """
    Combine user registration and image upload functionalities.
    """
    parser_classes = [FormParser, MultiPartParser]
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            if 'image' in self.request.data:
                return [IsAuthenticated()]
            return [AllowAny()]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for user registration instructions.
        """
        return CustomResponse.success({
            "status": "success",
            "message": "Veuillez envoyer une requête POST pour vous inscrire ou mettre à jour une image.",
        }, status_code=200)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for both user registration and image upload.
        """
        logger.info("Handling POST request in RegisterUserView.")
        logger.debug(f"Request data: {request.data}")
        logger.debug(f"Request files: {request.FILES}")

        if 'image' in request.FILES:
            # Handle image upload
            return self.handle_image_upload(request)
        else:
            # Handle user registration
            return self.handle_user_registration(request)


    def handle_user_registration(self, request):
        """
        Process user registration.
        """
        logger.info("Starting user registration process.")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User {user.username} created successfully.")

            # Check if an image is included in the request
            if 'image' in request.FILES:
                logger.debug("Handling image upload during user registration.")
                image_serializer = PlayerImageUploadSerializer(instance=user, data=request.data, partial=True)
                if image_serializer.is_valid():
                    image_serializer.save()
                    logger.info(f"Image uploaded successfully for user {user.username}.")
                else:
                    logger.warning(f"Image upload failed: {image_serializer.errors}")

            return CustomResponse.success(
                {"CustomUser": "created"},
                status_code=201
            )
        logger.warning(f"User registration failed: {serializer.errors}")
        return CustomResponse.error(
            {"errors": serializer.errors},
            status_code=400
        )
        
    def handle_image_upload(self, request):
        """
        Process image upload for authenticated users.
        """
        logger.info("Handling image upload for authenticated user.")
        user = request.user
        serializer = PlayerImageUploadSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            logger.debug("Serializer is valid. Saving image...")
            serializer.save()
            logger.info(f"Image uploaded successfully for user {user.username}.")
            return CustomResponse.success(
                {"message": "Image uploaded successfully.", "data": serializer.data},
                status_code=200
            )
        logger.warning(f"Image upload failed: {serializer.errors}")
        return CustomResponse.error(
            {"errors": serializer.errors},
            status_code=400
        )


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
                {"errors": "champ vide"},
                status_code=400
        ))
        else:
            return(CustomResponse.error(
                {"errors": "le pseudo ou le mdp n'est pas valide"},
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
    
    user.username = f"user_{user.id}"
    user.image = None 
    user.is_anonymized = True
    user.save()
    
 # \\___________Healthcheck pour docker________________//       
     
            
class HealthCheckView(APIView):
    
    def get(self, request):
        return (CustomResponse.success(
            {"status": "ok"},
            status_code=200
        ))
            
''''
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
# class DeleteAccountView(APIView):
    
#     def delete(self, request, *args, **kwargs):
        
#         user = request.user
#         if user.is_authenticated:
#             anonymize_and_delete_user(user)
#             return Response({"message": "Votre compte a été supprimé et anonymisé."}, status=200)
#         return Response({"error": "Utilisateur non authentifié."}, status=401)