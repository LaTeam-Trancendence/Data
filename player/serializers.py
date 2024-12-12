from rest_framework import serializers
from tables_core.models import CustomUser, Player, Match
from register.serializers import UserSerializer
from PIL import Image


# \\ _______________________________________________//


class PlayerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Player
        fields = ['id', 'user', 'friends', 'status', 'win_pong', 'lose_pong',
                  'win_tictactoe', 'lose_tictactoe']

    def create(self, validated_data):

        if 'user' not in validated_data:
            raise serializers.ValidationError({"user": "Un utilisateur doit être spécifié."})
        return super().create(validated_data)

    # protection contre les injection sql
    # Vérifie le type MIME permet d'identifier la nature et le format de docs
    # Vérifie la taille du fichier (max 5MB)

class PlayerImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['image'] #inclu uniquement le champ image


    def update(self, instance, validated_data):
        instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance

class PlayerStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "user", "win_pong", "lose_pong", "win_tictactoe", "lose_tictactoe"]


class StatUpdateSerializer(serializers.Serializer):
    stat_type = serializers.ChoiceField(
        choices=["win_pong", "lose_pong", "win_tictactoe", "lose_tictactoe"]
    )
    ''''
    def validate_profile_picture(self, value):

        if value.content_type not in ['image/jpeg', 'image/png']:
            raise serializers.ValidationError("Seuls les fichiers JPEG et PNG sont autorisés.")

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("La taille maximale est de 5MB.")

        try:
            img = Image.open(value)
            img.verify()  # Vérifie si c'est une image valide
            if img.height > 400 or img.width > 400:
                raise serializers.ValidationError("Les dimensions de l'image doivent être de 400x400 pixels maximum.")

        except (IOError, SyntaxError):
            raise serializers.ValidationError("Fichier invalide. Téléchargez une image valide.")

        return value

        '''
# class DisplayPlayerSerializer(serializers.ModelSerializer):
#     player = serializers.SerializerMethodField()

#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'player']

#     def get_player(self, obj):
#         try:
#             player = Player.objects.get(user=obj)
#             return PlayerSerializer(player).data
#         except Player.DoesNotExist:
#             return None

