from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Post, Comment
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, CommentDetailSerializer


def get_comments(request):
    comments = Comment.objects.filter(level__lt=4).select_related('parent').order_by('creation_date')
    for comment in comments:
        json_data = {
            "id": comment.pk,
            "post": comment.post,
            "text": comment.text,
            "creation_date": comment.creation_date,
            "children": comment.children,
        }
        #if comment.parent:

#        print(json_data)

    return

