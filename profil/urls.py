from django.urls import path
from .views import DisplayPlayerView, ListPlayerView 
from .views import AddFriendsView, MatchResultView


# \\_______________________________________________//


urlpatterns = [
    path('profil/', DisplayPlayerView.as_view(), name='profil'),
    path('ListPlayers/', ListPlayerView.as_view(), name='ListPlayers'),
    path('AddFriends/', AddFriendsView.as_view(), name='AddFriends'),
    path('ResultPong/', MatchResultView.as_view(), name='ResultPong')
]