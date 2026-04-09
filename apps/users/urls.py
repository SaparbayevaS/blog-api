from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,  TokenRefreshView
from .views import RegisterViewSet, UserSettingsViewSet

register = RegisterViewSet.as_view({'post': 'create'})
change_language = UserSettingsViewSet.as_view({'patch': 'change_language'})
change_timezone = UserSettingsViewSet.as_view({'patch': 'change_timezone'})
urlpatterns = [
    path('auth/register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('auth/language/'. change_language, name='change_language'),
    path('auth/timezone/', change_timezone, name='change_timezone'),
]
