from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from apps.blog.models import Post, Category, Tag

User = get_user_model()

class Command(BaseCommand):
    help = "Seed test data"

    def handle(self, *args, **kwargs):
        user = User.objects.create_user(
            email="examplen@example.com",
            password="example",
            first_name="example",
            last_name="example"
        )

        cat = Category.objects.create(name="Tech", slug="tech")

        tag = Tag.objects.create(name="Django", slug="django")

        post = Post.objects.create(
            author=user,
            title="Test Post 2",
            slug="test-post2",
            body="wannasleep",
            category=cat,
            status=Post.Status.PUBLISHED
        )

        post.tags.add(tag)

        self.stdout.write(self.style.SUCCESS("Seed data created"))
