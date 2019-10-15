from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

# TODO remove unused urls in the end
from accounts.views import RegisterView

urlpatterns = [
    path(r'', include("accounts.urls")),
    path(r'', include("blog.urls")),
    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('admin/', admin.site.urls),
]
