from django.urls import path
from .views import FinalizeMatchView


# \\_______________________________________________//

urlpatterns = [
    path('match/', FinalizeMatchView.as_view(), name='listmatch'),
    path('match/<int:match_id>/', FinalizeMatchView.as_view(),
         name='statMatch'),
]
