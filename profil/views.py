from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from tables_core.models import CustomUser, Player, Match
from django.core.files.storage import FileSystemStorage
from register.utils import CustomResponse
from .serializers import ListPlayerSerializer, CustomPlayerSerializer, FriendSerializer
from Back import settings
import logging


# \\______________profil____________//

class DisplayPlayerView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
			player = Player.objects.get(user=request.user)
			print(player.user.image)
			print(player.user.username)
			serializer = CustomPlayerSerializer(player)
			return(CustomResponse.success(
				serializer.data,
				status_code=200
			))
			
	def put(self, request):
		player = Player.objects.get(user=request.user)
		print(player)
		
		# //________status_________\\
			
		status = request.data.get('status')

		if status:
			player.status = status
			player.save()
			return CustomResponse.success(
				{"status": "updated"},
				status_code=200)
		
		# //________pseudo_________\\

		username = request.data.get('username')
		if username:
			player.user.username = username
			player.user.save()
			print(username)
			return CustomResponse.success(
				{"pseudo": "updated"},
				status_code=200)


		# //________password_________\\

		password = request.data.get('password')

		if password:
			player.user.set_password(password)
			player.user.save()
			print(password)
			update_session_auth_hash(request, player.user)
			return CustomResponse.success(
				{"passowrd": "updated"},
				status_code=200)
		
		# //________image_________\\


		image = request.FILES.get('img')

		print(image)
		if image:

			fs = FileSystemStorage(location=settings.MEDIA_ROOT)
			filename = fs.save('player_picture/' + image.name, image)
			file_url = fs.url(filename)
	
			player.user.image = file_url
			player.user.save()

		# image = request.data.get('image')

		# if image:
		# 	player.user.image = image
		# 	print(image)
		# 	player.user.save()
		# 	return CustomResponse.success(
		# 		{"image": "updated"},
		# 		status_code=200)
			
			
		return CustomResponse.error(
				{"saisie non valide"},
				status_code=400)
			
	# def put(self, request):
	#     user = request.user
	#     serializer = CustomPlayerSerializer(user)
	#     if serializer.is_valid():
	#         serializer.save()
	#         return CustomResponse.success(
	#             {"Modif": "ok"}, status_code=200)
			
			
		# else:
		#     return CustomResponse.error(
		#         {"No status provided"}, status_code=400)

  
# \\___________gestion friends______________//
		
class AddFriendsView(APIView):
	permission_classes = [IsAuthenticated]
	
	def post(self, request):
		player = Player.objects.get(user=request.user)
		friend_username = request.data.get("friend_username")
		
		try:
			friend = Player.objects.get(user__username=friend_username)
			if friend in player.friends.all():
				return (CustomResponse.error(
					{"message": "Ce joueur est déjà dans votre liste d'amis."},
					status_code=400
					))
			player.friends.add(friend)
			player.save()
			return (CustomResponse.success(
				{"message": "ami ajouté avec succes."},
				status_code=200
				))

		except Player.DoesNotExist:
			return CustomResponse.error(
       			{"error": "joueur non trouvé"},
          		status_code=404)


# \\______________listPlayer____________//

		
class ListPlayerView(APIView):
	permission_classes = [IsAuthenticated]
	
	def get(self, request):
		player = Player.objects.all()
		serializer = ListPlayerSerializer(player, many=True)
		return(CustomResponse.success(
			serializer.data,
			status_code=200
		))
		
class MatchResultView(APIView):
	permission_classes = [IsAuthenticated]
	
	def post(self, request):
		player = Player.objects.get(user=request.user)
		result = request.data.get('result')
		
		if result == 'win_pong':
			player.win_pong += 1
		elif result == 'lose_pong':
			player.lose_pong += 1
		player.save()
		return CustomResponse.success(
				{"match": "updated"}, status_code=200)