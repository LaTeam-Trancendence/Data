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
        extra_kwargs = {'password': {'write_only': True}}


    def validate_password(self, value):

        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    # def get_image_url(self, obj):
    #     # Retourne l'URL complète de l'image si elle existe, sinon retourne None
    #     return obj.image.url if obj.image else None
    
    def create(self, validated_data):
        username = validated_data['username']
        image = validated_data.pop('image', None)
        

        # Sauvegarder le fichier image si présent
        if image:
            ext = os.path.splitext(image.name)[1]

            valid_extensions = ['.png']
            if ext not in valid_extensions:
                ext == ['.png'],
            image_name = f"{username}{'.png'}"
        
            fs = FileSystemStorage(location=os.path.join(str(settings.MEDIA_ROOT), 'player_picture'))
            filename = fs.save(image_name, image)
            validated_data['image'] = f"player_picture/{filename}"
        else:
   
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'player_picture', 'default_avatar.png')
            image_name = f"{username}.png"
            
            with open(default_image_path, 'rb') as default_image:
                with open(os.path.join(settings.MEDIA_ROOT, 'player_picture', image_name), 'wb') as new_image:
                    new_image.write(default_image.read())
            
            validated_data['image'] = f"player_picture/{image_name}"

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            image=validated_data.get('image')
        )
        
        return user
    


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

class PlayerImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["image"] 
''''
    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance
'''