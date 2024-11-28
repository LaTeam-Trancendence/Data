from django.db import models



from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, 
                related_name="player") 

    friends = models.models.ManyToManyField("self", symetrical=True, blank=True)
    
    def __str__(self):
        return self.user.username