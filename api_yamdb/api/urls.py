from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
]
