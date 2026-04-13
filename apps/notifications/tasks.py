from celery import shared_task
from apps.notifications.models import Notification
from apps.blog.models import Comment
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


from django.utils import timezone
from datetime import timedelta

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retriess=3
)
def process_new_comment(comment_id):
    comment = Comment.objects.select_related("post", "author").get(id=comment_id)
    post = comment.post

    if post.author != comment.author:
        Notification.objects.create(
            recipient=post.author,
            comment=comment
        )
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"post_{post.slug}",
        {
            "type": "comment_message",
            "message": {
                "comment_id": comment.id,
                "author": {
                    "id": comment.author.id,
                    "email": comment.author.email,
                },
                "body": comment.body,
                "created_at": str(comment.created_at),
            },
        },
    )

@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retriess=3
)
def clear_expireed_notifications():
    limit = timezone.now() - timedelta(days=30)
    Notification.objects.filter(created_at__lt=limit).delete()