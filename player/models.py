from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# //_____________________//

# dans AbstractUser les champs username et password sont deja crees
# username = max 150 char et password = deja hashe
# ajouter pour limiter la taille :
#       short_name = models.CharField(unique=True, max_length=15)
# Reste a gerer les amis en intergrant une liste

class Player(AbstractUser):

    profile_picture = models.TextField(null=True)
    language = models.CharField(max_length=2, default="FR")
    
    #friends
    status = models.BooleanField(default=False)
    
    win_pong = models.IntegerField(default=0)
    lose_pong = models.IntegerField(default=0)
    
    win_tictactoe = models.IntegerField(default=0)
    lose_tictactoe = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username
    