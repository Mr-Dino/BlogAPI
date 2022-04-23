from rest_framework import serializers
from .models import Post, Comment
from rest_framework.serializers import ReturnDict


class NoParentSerializer(serializers.ListSerializer):
    """Сериализатор для вывода элементов у которых нет родителя"""

    def to_representation(self, data):
        data = data.filter(parent=None).select_related('parent')
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Рекурсивынй вывод дочерних элементов"""

    def __init__(self, **kwargs):
        self._recurse_max = 4
        super(RecursiveSerializer, self).__init__(**kwargs)

    def to_representation(self, data):
        serializer = self.parent.parent.__class__(data, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения всех комментариев"""

    children = RecursiveSerializer(many=True)
    # children = serializers.PrimaryKeyRelatedField()

    class Meta:
        list_serializer_class = NoParentSerializer
        model = Comment
        fields = ('id', 'level', 'post', 'creation_date', 'children')



class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения всех постов"""

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'creation_date')


class PostDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального отображения постов"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'creation_date', 'content')




class CommentDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального отображения комментария"""

    class Meta:
        model = Comment
        fields = ('id', 'post', 'creation_date', 'parent', 'text')


