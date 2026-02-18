from django.db.models import Model, CharField, SlugField, TextChoices, ForeignKey, TextField, CASCADE, SET_NULL, ManyToManyField, DateTimeField
from apps.users.models import User

class Category(Model):
    name = CharField(max_length=100, unique=True)
    slug = SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Tag(Model):
    name = CharField(max_length=50, unique=True)
    slug = SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Post(Model):
    class Status(TextChoices):
        DRAFT = 'draft'
        PUBLISHED = 'published'

    author = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=200)
    slug = SlugField(unique=True) 
    body = TextField()
    category = ForeignKey(Category, null=True, on_delete=SET_NULL)
    tags = ManyToManyField(Tag, blank=True)
    status = CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(Model):
    post = ForeignKey(Post, on_delete=CASCADE, related_name='commments')
    author = ForeignKey(User, on_delete=CASCADE)
    body = TextField()
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by {self.author.email} on {self.post.title}"
