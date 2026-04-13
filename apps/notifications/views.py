from django.shortcuts import render
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_count(request):
    count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
        ).count()
    
    return Response({"unread_count": count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notification_list(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True)

    return Response({"status": "ok"})
