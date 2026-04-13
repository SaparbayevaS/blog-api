from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import Post, Comment, Category, Tag

class CategorySerializer(ModelSerializer):
    class Meta: 
        model = Category
        fields = '__all__'

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'