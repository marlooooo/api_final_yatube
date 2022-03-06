from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet, GroupViewSet, FollowViewSet

router = DefaultRouter()

router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include('djoser.urls'), name='djoser_v1'),
    path('v1/', include('djoser.urls.jwt'), name='djoser_jwt_v1'),
    path('v1/', include(router.urls), name='router_v1')
]
