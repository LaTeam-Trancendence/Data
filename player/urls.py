from django.urls import path
from .views import statsPlayerView, changeImageAPIView, signupAPIView


# \\_______________________________________________//

urlpatterns = [
    path('players/', statsPlayerView.as_view(), name='listPlayer'),
    path('players/<int:player_id>/', statsPlayerView.as_view(), 
         name='statPlayers'),
#    path('image/', UploadPlayerImageView.as_view(), name='imagePlayer'),
    path('image/', changeImageAPIView.as_view(), name='image'),
    path('imageAjout/', signupAPIView.as_view(), name='imagePlayerAjout')
]
