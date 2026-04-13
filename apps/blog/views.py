from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.notifications.models import Notification
import logging
from apps.notifications.tasks import process_new_comment
import json
import asyncio
from django.http import StreamingHttpResponse

logger = logging.getLogger('apps.blog')


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        lang = getattr(request, "LANGUAGE_CODE", "en")
        cache_key = f'published_posts_{lang}'

        cached_posts = cache.get('published_posts')
        if cached_posts:
            logger.debug("Returning cached posts")
            return Response(cached_posts)

        queryset = self.get_queryset().filter(status=Post.Status.PUBLISHED)
        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, timeout=60)
        logger.debug("Posts cached for language: %s", lang)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        for l in ['en', 'ru', 'kk']:
            cache.delete(f'published_posts_{l}')
        logger.info(
            'Post created by user %s: %s',
            self.request.user.email,
            serializer.instance.slug
        )

    def perform_update(self, serializer):
        serializer.save()
        for l in ['en', 'ru', 'kk']:
            cache.delete(f'published_posts_{l}')
        logger.info(
            'Post updated by user %s: %s',
            self.request.user.email,
            serializer.instance.slug
        )

    def perform_destroy(self, instance):
        for l in ['en', 'ru', 'kk']:
            cache.delete(f'published_posts_{l}')
        logger.warning(
            'Post deleted by user %s: %s',
            self.request.user.email,
            instance.slug
        )
        instance.delete()

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, slug=None):
        post = self.get_object()

        if request.method == 'GET':
            serializer = CommentSerializer(Comment.objects.filter(post=post), many=True)
            logger.debug('Comments fetched for post %s', post.slug)
            return Response(serializer.data)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, post=post)

            process_new_comment.delay(comment.id)

            logger.info(
                "New comment by %s on post %s",
                request.user.email,
                post.slug
            )


            return Response(CommentSerializer(comment).data, status=201)

        return Response(serializer.errors, status=400)
    

async def post_stream(request):
    async def event_stream():
        last_id = 0

        while True:
            def get_posts():
                return list(
                    Post.objects.filter(
                        status=Post.Status.PUBLISHED,
                        id__gt=last_id
                    ).select_related("author").order_by("id")
                )
            posts = await asyncio.to_thread(get_posts)

            for post in posts:
                data = {
                    "post_id": post.id,
                    "title": post.title,
                    "slug": post.slug,
                    "author": {
                        "id": post.author.id,
                        "email": post.author.email,
                    },
                    "published_at": str(post.created_at),
                }

                yield f"data: {json.dumps(data)}\n\n"
                last_id = post.id

            await asyncio.sleep(2)

    return StreamingHttpResponse(
        event_stream(),
        content_type="text/event-stream"
    )
