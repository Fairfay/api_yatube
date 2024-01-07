from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from posts.models import Post, Comment, Group
from .serializers import (ApiPostSerializer,
                          ApiCommentSerializer,
                          GroupSerializer)


class ApiPostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = ApiPostSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ApiPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = ApiPostSerializer
    authentication_classes = [TokenAuthentication]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.author:
            return Response({"detail": "Не трогай чужое"},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.author:
            return Response({"detail": "Не трогай чужое"},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class ApiGroupListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [TokenAuthentication]


class ApiGroupDetailView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [TokenAuthentication]


class ApiCommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = ApiCommentSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        if not post_id:
            post_id = self.kwargs.get('post_id')
        post = None
        if post_id:
            post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)


class ApiCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = ApiCommentSerializer
    authentication_classes = [TokenAuthentication]
    lookup_url_kwarg = 'comment_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.author:
            return Response({"detail": "Не трогай чужое"},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.author:
            return Response({"detail": "Не трогай чужое"},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
