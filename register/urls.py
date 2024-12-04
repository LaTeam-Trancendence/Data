from django.urls import path
from .views import RegisterUserView, LoginView, LogoutView, HealthCheckView, DeleteAccountView


# \\_______________________________________________//


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', DeleteAccountView.as_view(), name='delete'),
    path('healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
]