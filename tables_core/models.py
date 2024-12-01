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
    image = models.ImageField(upload_to='media/player_picture/', blank=True, null=True)
    
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
    
    #username = 
    #password = 
    #picture =

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, 
                related_name="player") 
    
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)
    
    language = models.CharField(max_length=2, default="FR")
    
    #friends
    status = models.BooleanField(default=False)
    
    win_pong = models.IntegerField(default=0)
    lose_pong = models.IntegerField(default=0)
    
    win_tictactoe = models.IntegerField(default=0)
    lose_tictactoe = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    
    """property ajoutes des propietes dynamiques aux models sans data, Calcul du total de parties jouées en temps reel."""  
    @property
    def total_games(self):
        return self.win_pong + self.lose_pong + self.win_tictactoe + self.lose_tictactoe

    """Calcul du pourcentage de victoires."""
    @property
    def win_rate(self):
        total_games = self.total_games
        if total_games == 0:
            return 0
        total_wins = self.win_pong + self.win_tictactoe
        return round((total_wins / total_games) * 100, 2)
    
# //________________________________________________\\

class Match(models.Model):
    
    user = models.ForeignKey(Player, on_delete=models.CASCADE, 
                        related_name='user_matches')
    adv = models.ForeignKey(Player, on_delete=models.SET_NULL, 
                        null=True, related_name='adv_matches')
    
    user_score = models.IntegerField(default=0)
    adv_score = models.IntegerField(default=0)
    result = models.IntegerField(default=0)
    
    date = models.DateTimeField(null=True)
    start_match = models.DateTimeField(null=True)
    end_match = models.DateTimeField(null=True)
    duration = models.DurationField(null=True)
    
    # def __str__(self):
    #     return f"Match {self.id} - {self.user} vs {self.adv}"
    
    
    
    def save(self, *args, **kwargs):
        if self.start_match and self.end_match:
            self.duration = self.end_match - self.start_match 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Match {self.id} - {self.user} vs {self.adv}"