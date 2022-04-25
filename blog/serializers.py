from rest_framework import serializers
from .models import Post, Comment


class PostCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения  постов"""

    class Meta:
        model = Post
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания комментария к посту"""

    class Meta:
        model = Comment
        fields = ('text', 'parent', 'post')