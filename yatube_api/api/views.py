from django.apps import apps
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from .mixins import ListCreateViewSet
from .serializers import (
    CommentSerializer, PostSerializer, GroupSerializer, FollowSerializer
)


# вместо from post.models import Group, Post
Group = apps.get_model(app_label='posts', model_name='Group')
Post = apps.get_model(app_label='posts', model_name='Post')


class PostViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обрабатывает все виды запросов, связанные с моделью Post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет обрабатывает получение и создание объектов класса Group
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обрабатывает все виды запросов связанных с моделью Comment.
    """

    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(ListCreateViewSet):
    """
    Вьюсет используется для обработки запросов создания и получения списка
    объектов класса Follow.
    """

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    search_fields = ('following__username', 'user__username')
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
