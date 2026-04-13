from django.db.models import Model, ForeignKey, CASCADE, BooleanField, DateTimeField
from apps.blog.models import Comment
from django.conf import settings


# Create your models here.
class Notification(Model):
    recipient = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name='notifications')
    comment = ForeignKey(Comment, on_delete=CASCADE, related_name='notifications')
    is_read =  BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient}'