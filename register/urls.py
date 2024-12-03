from django.urls import path
from .views import RegisterUserView, LoginView, HealthCheckView


# \\_______________________________________________//


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LoginView.as_view(), name='logout'),
    path('healtcheck/', HealthCheckView.as_view(), name='healtcheck'),
]