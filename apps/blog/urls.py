from rest_framework.routers import DefaultRouter
from .views import PostViewSet, post_stream
from .views_stats import StatsAPIView
from django.urls import path

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = router.urls
urlpatterns += [
    path('stats/', StatsAPIView.as_view(), name='stats'),

    path('stream/', post_stream),
]