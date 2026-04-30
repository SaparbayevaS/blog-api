from celery import shared_task
from django.core.cache import cache
from apps.blog.models import Post, Comment
from django.utils import timezone
from datetime import timedelta
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

from django.contrib.auth import get_user_model
User = get_user_model()
logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def invalidate_posts_cache():
    cache.clear()


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def publish_scheduled_posts():
    posts = Post.objects.filter(
        status=Post.Status.SCHEDULED,
        publish_at__lte=timezone.now()
    )

    channel_layer = get_channel_layer()

    for post in posts:
        post.status = Post.Status.PUBLISHED
        post.save()

        async_to_sync(channel_layer.group_send)(
            "posts_stream",
            {
                "type": "post_published",
                "message": {
                    "post_id": post.id,
                    "title": post.title,
                    "slug": post.slug,
                    "author": {
                        "id": post.author.id,
                        "email": post.author.email,
                    },
                    "published_at": str(post.created_at),
                },
            }
        )


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def generate_daily_stats():
    now = timezone.now()
    yesterday = now - timedelta(days=1)

    posts = Post.objects.filter(created_at__gte=yesterday).count()
    comments = Comment.objects.filter(created_at__gte=yesterday).count()
    users = User.objects.filter(date_joined__gte=yesterday).count()

    logger.info(
        "DAILY STATS -> posts=%s comments=%s users=%s",
        posts, comments, users
    )