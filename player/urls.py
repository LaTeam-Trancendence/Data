from django.urls import path
from .views import statsPlayerView, PlayerStatAPIView, PlayerDetailAPIView


# \\_______________________________________________//

urlpatterns = [
    path('players/', statsPlayerView.as_view(), name='listPlayer'),
    path('players/<int:player_id>/', statsPlayerView.as_view(),
         name='statPlayers'),
    path('players/<int:pk>/<str:stat_type>/', PlayerStatAPIView.as_view(), name="stats"),
    path('players/<int:pk>/', PlayerDetailAPIView.as_view(), name="statsVIEW")
#    path('image/', UploadPlayerImageView.as_view(), name='imagePlayer'),
#    path('image/', changeImageAPIView.as_view(), name='image'),
#    path('imageAjout/', signupAPIView.as_view(), name='imagePlayerAjout')
]
