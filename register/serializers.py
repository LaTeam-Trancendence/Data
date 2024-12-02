from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from tables_core.models import CustomUser, Player, Match
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password 
from Back import settings

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
        
        user = CustomUser.objects.create_user(
                                username=validated_data['username'],
                                password=validated_data['password'],
                                image=validated_data.get('image', None),
        )
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

