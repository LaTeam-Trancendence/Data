from django.urls import path
from .views import DisplayPlayerView, ListPlayerView


# \\_______________________________________________//


urlpatterns = [
    path('profil/', DisplayPlayerView.as_view(), name='profil'),
    path('ListPlayers/', ListPlayerView.as_view(), name='ListPlayers')
]