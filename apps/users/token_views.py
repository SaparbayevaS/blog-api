from django.utils.decorators import method_decorator
from rest_framework_simplejwt.views import TokenObtainPairView
from django_ratelimit.decorators import ratelimit
import logging

logger = logging.getLogger('apps.users')

@method_decorator(
    ratelimit(
        key='ip',
        rate='10/m',
        method='POST',
        block=True
    ),
    name='post'
)
class RateLimitedTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        logger.info("Login attempt from IP")
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            logger.info('Login success')
        else:
            logger.info('Lofin failed')
        return response