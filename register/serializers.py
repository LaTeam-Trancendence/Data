from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tables_core.models import CustomUser, Player, Match
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.password_validation import validate_password 
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.core.files.storage import FileSystemStorage
from Back import settings
import os

# \\_______________register______________________________//

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'image']
        # extra_kwargs = {'password': {'write_only': True}}


    def validate_password(self, value):

        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def create(self, validated_data):
        image = validated_data.pop('image', None)
        
        # Sauvegarder le fichier image si présent
        if image:
            fs = FileSystemStorage(location=os.path.join(str(settings.MEDIA_ROOT), 'player_picture'))
            filename = fs.save(image.name, image)
            validated_data['image'] = 'player_picture/' + filename

        # Créer l'utilisateur avec les données validées
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            image=validated_data.get('image')
        )
        
    # def create(self, validated_data):
    #     print(validated_data)
    #     image=validated_data.pop('image', None),
    #     print(image)
    #     user = CustomUser.objects.create_user(
    #                             username=validated_data['username'],
    #                             password=validated_data['password'],
    #     )

    #     if image:
    #         if isinstance(image, tuple):
    #             image = image[0]

    #         if isinstance(image, (InMemoryUploadedFile, TemporaryUploadedFile)):    
    #             fs = FileSystemStorage(location=settings.MEDIA_ROOT)
    #             filename = fs.save('player_picture/' + image.name, image)
    #             user.image = fs.url(filename)
    #             user.save()
        # player = Player.objects.create_user()
        return user

    
# \\__________________login_______________________________//


class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Identifiants non valides")
        data["user"] = user
        return data
    

class DeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

    def validate_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("L'ID doit être positif.")
        return value

