from django.urls import path
from .views import notification_count, notification_list, mark_all_as_read

urlpatterns = [
    path('count/', notification_count),
    path('', notification_list),
    path('read/', mark_all_as_read)
]