from django.urls import path
from .views import statsPlayerView
from .views import PlayerCreateView

# \\_______________________________________________//

urlpatterns = [
    path('players/', statsPlayerView.as_view(), name='listPlayer'),
    path('players/<int:player_id>/', statsPlayerView.as_view(), 
         name='statPlayers'),
    path('playertest/', PlayerCreateView.as_view(), name='listtest'),
]
