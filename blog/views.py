from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics

from .models import Post, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, CommentDetailSerializer


@api_view(['GET', 'POST'])
def api_posts(request):
    """
    Получение всех постов и комментариев с уровнем вложенности до 3
    Создание нового поста
    """
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIComments(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = None

    def get_queryset(self):
        comments = Comment.objects.filter(level__lt=4).select_related("parent")
        return comments


@api_view(['GET', 'POST'])
def api_comments(request):
    """
    Получение комментариев с уровнем вложенности до 3
    Созднаие комментария
    """
    if request.method == "GET":
        comments = Comment.objects.filter(level__lt=4).select_related('parent')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_post_detail(request, pk):
    """
    Получение отдельных поста
    Исправление всех полей поста
    Исправление отдельных полей
    Удаление поста
    """
    post = Post.objects.get(pk=pk)
    if request.method == "GET":
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT" or request.method == "PATCH":
        serializer = PostDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_comment_detail(request, pk):
    """
    Получение конкретного комментария
    Исправление всех полей комментария
    Исправление отдельных полей комментария
    Удаление комментария
    """
    comment = Comment.objects.get(pk=pk)
    if request.method == "GET":
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)
    elif request.method == "PUT" or request.method == "PATCH":
        serializer = CommentDetailSerializer(comment, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""class APIPosts(APIView):

    def get(self, request):
        posts = Comment.objects.filter(level__lte=4).select_related('post')
        serializer = CommentSerializer(posts, many=True)
        return Response(serializer.data)"""
