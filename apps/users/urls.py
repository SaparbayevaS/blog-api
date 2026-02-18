from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,  TokenRefreshView
from .views import RegisterViewSet

register = RegisterViewSet.as_view({'post': 'register'})
urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
