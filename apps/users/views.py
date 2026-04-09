from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LanguageSerializer, TimezoneSerializer
import logging
from django.contrib.auth import get_user_model
from django_ratelimit.decorators import ratelimit, action
from django.utils.decorators import method_decorator

logger = logging.getLogger('apps.users')
User = get_user_model()

class RegisterViewSet(ViewSet):
    permission_classes = [AllowAny]
    @method_decorator(
            ratelimit(
                key='ip',
                rate='5/m',
                method='POST',
                block=True
            )
    )

    def create(self, request):
        logger.info('Registration attempt for email: %s', request.data.get('email'))

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            logger.info('User registered: %s', user.email)

            return Response({
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=HTTP_201_CREATED)

        logger.warning('Registration failed: %s', serializer.errors)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class UserSettingsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=["patch"], url_path="timezone")
    def change_language(self, request):
        serializer = LanguageSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Language updated"})
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["patch"], url_path="timezone")
    def change_timezone(self, request):
        serializer = TimezoneSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Timezone updated"})
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)