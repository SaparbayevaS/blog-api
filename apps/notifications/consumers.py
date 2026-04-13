import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.blog.models import Post, Comment
from django.contrib.auth import get_user_model

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.slug = self.scope['url_route']['kwargs']['slug']
        self.group_name = f"post_{self.slug}"

        try:
            self.post = await Post.objects.aget(slug=self.slug)
        except Post.DoesNotExist:
            await self.close(code=4004)


        token = self.scope['query_string'].decode().split('=')[1]
        if not token:
            await self.clode(code=4001)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def comment_message(self, event):
        await self.send(text_data=json.dumps(event['message']))