from django.urls import path

from . import views

urlpatterns = [
    path("api/post/<int:post_id>/", views.get_post_comments, name="comments_to_post"),
    path("api/create/post/", views.create_post, name="post_create"),
    path("api/create/comment/", views.create_comment, name="comment_to_post"),
    path("api/comment/<int:comment_id>/", views.get_all_comments, name="comment_comments"),
]

