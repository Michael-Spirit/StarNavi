from django.urls import path, include
from rest_framework import routers
from accounts.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-user/', include('rest_framework.urls', namespace='rest_framework'))
]
