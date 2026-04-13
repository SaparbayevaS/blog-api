from rest_framework.serializers import ModelSerializer
from .models import Notification

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'comment', 'is_read', 'created_at']