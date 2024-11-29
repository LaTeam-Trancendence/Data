from django.urls import path
from .views import statsPlayerView, PlayerUpdateView


# \\_______________________________________________//

urlpatterns = [
    path('players/', statsPlayerView.as_view(), name='listPlayer'),
    path('players/<int:player_id>/', statsPlayerView.as_view(), 
         name='statPlayers'),
    path('image/', PlayerUpdateView.as_view(), name='imagePlayer')
]
