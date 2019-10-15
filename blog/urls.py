from django.urls import path, include
from rest_framework import routers
from blog.views import PostViewSet, VoteViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
