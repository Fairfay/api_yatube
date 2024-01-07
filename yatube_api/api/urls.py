from django.urls import path
from .views import (ApiPostListCreateView,
                    ApiPostDetailView,
                    ApiGroupListView,
                    ApiGroupDetailView,
                    ApiCommentListCreateView,
                    ApiCommentDetailView)
from rest_framework.authtoken import views

urlpatterns = [
    path('api-token-auth/',
         views.obtain_auth_token),
    path('posts/',
         ApiPostListCreateView.as_view(),
         name='api-post-list-create'),
    path('posts/<int:pk>/',
         ApiPostDetailView.as_view(),
         name='api-post-detail'),
    path('groups/',
         ApiGroupListView.as_view(),
         name='api-group-list'),
    path('groups/<int:pk>/',
         ApiGroupDetailView.as_view(),
         name='api-group-detail'),
    path('posts/<int:post_id>/comments/',
         ApiCommentListCreateView.as_view(),
         name='api-comment-list-create'),
    path('posts/<int:post_id>/comments/<int:comment_id>/',
         ApiCommentDetailView.as_view(),
         name='api-comment-detail'),
]
