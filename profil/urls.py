from django.urls import path
from .views import DisplayPlayerView


# \\_______________________________________________//


urlpatterns = [
    path('profil/', DisplayPlayerView.as_view(), name='profil'),
]