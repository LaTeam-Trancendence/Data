from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# //__________________________________________________\\
# dans AbstractUser les champs username et password sont deja crees
# username = max 150 char et password = deja hashe
# ajouter pour limiter la taille :
#       short_name = models.CharField(unique=True, max_length=15)

# group : pour gerer les permissions pas tres utile mais fonctionne :)

# Reste a gerer les amis en intergrant une liste

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='images_pics/', blank=True, null=True)
    
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name="custom_user_groups",  
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name="custom_user_permissions", 
    #     blank=True,
    # )
# //________________________________________________\\

# OneToOneField = un user pour un player

class Player(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="player") 
    
    language = models.CharField(max_length=2, default="FR")
    
    #friends
    status = models.BooleanField(default=False)
    
    win_pong = models.IntegerField(default=0)
    lose_pong = models.IntegerField(default=0)
    
    win_tictactoe = models.IntegerField(default=0)
    lose_tictactoe = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username