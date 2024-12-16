import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tables_core.models import CustomUser
from django.conf import settings

class Command(BaseCommand):
    help = 'Anonymize inactive users'

    def handle(self, *args, **kwargs):
        threshold_date = timezone.now() - timedelta(days=30)  # Anonymiser après 30 jours d'inactivité

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

        user.username = f"user_{user.id}"
        user.image = None
        user.is_anonymized = True
        user.save()
