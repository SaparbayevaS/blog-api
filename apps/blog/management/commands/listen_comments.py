from asyncio import run
import json
from aioredis import from_url
from django.core.management.base import BaseCommand

REDIS_CHANNEL = "comments"

class Command(BaseCommand):
    help = "Listen for new comment events in Redis"

    def handle(self, *args, **options):
        run(self.listen())

    async def listen(self):
        redis = await from_url("redis://localhost:6379/0")
        pubsub = redis.pubsub
        await pubsub.subscribe(REDIS_CHANNEL)
        self.stdout.write(self.style.SUCCESS(f"Listening for comments on channel '{REDIS_CHANNEL}'..."))

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            data = message["data"]
            if isinstance(data, bytes):
                data = data.decode("utf-8")

            try:
                comment = json.loads(data)
                self.stdout.write(self.style.SUCCESS(f"New comment: {json.dumps(comment, ensure_ascii=False)}"))

            except json.JSONDecodeError:
                self.stderr.write(f"Invalis JSON: {data}")