from rest_framework import serializers
from tables_core.models import CustomUser, Player, Match
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from Back import settings

# \\_______________register______________________________//

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'image']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(username=validated_data['username'],
                                        password=validated_data['password'],
                                        image=validated_data.get('image', None),
        )

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
            raise serializers.ValidationError("Invalid credentials. Please try again.")
        data["user"] = user
        return data

