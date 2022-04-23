from django.urls import path

from . import views

urlpatterns = [
    path("api/comments/", views.APIComments.as_view(), name="api_comments"),
    #path("api/posts/", views.api_posts, name="api_posts"),
    #path("api/rubric/<int:pk>/", views.api_post_detail, name="api_post_detail"),
    #path("api/comment/<int:pk>/", views.api_comment_detail, name="api_comment_detail"),
]
