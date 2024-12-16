import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tables_core.models import CustomUser
from django.conf import settings
from shutil import copyfile

class Command(BaseCommand):
    help = 'Anonymize inactive users'

    def handle(self, *args, **kwargs):
        threshold_date = timezone.now() - timedelta(seconds=30)  # Anonymiser après 30 jours d'inactivité

        users_to_anonymize = CustomUser.objects.filter(
            last_login__lt=threshold_date,
            is_anonymized=False
        )

        for user in users_to_anonymize:
            self.anoCustomUser(user)

        self.stdout.write(f"{users_to_anonymize.count()} users anonymized.")

    def anoCustomUser(self, user):
        if user.image:
            image_path = os.path.join(settings.MEDIA_ROOT, user.image.name)
            if os.path.isfile(image_path):
                os.remove(image_path)


        default_image_path = os.path.join(settings.MEDIA_ROOT, 'player_picture', 'default_avatar.png')
    
        # Vérifier si l'image par défaut existe
        if not os.path.isfile(default_image_path):
            raise FileNotFoundError(f"L'image par défaut {default_image_path} est introuvable.")
    
        # Créer une copie de l'image par défaut avec le nom personnalisé
        new_image_name = f"player_picture/user_{user.id}.png"
        new_image_path = os.path.join(settings.MEDIA_ROOT, new_image_name)
        copyfile(default_image_path, new_image_path)
        
        user.username = f"user_{user.id}"
        user.image = new_image_name
        user.is_anonymized = True
        user.save()
