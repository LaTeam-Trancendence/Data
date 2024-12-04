from django.urls import path
from .views import RegisterUserView, LoginView, LogoutView, HealthCheckView


# \\_______________________________________________//


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
]