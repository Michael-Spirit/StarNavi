import clearbit
from django.conf import settings
from requests import HTTPError

from accounts.models import User
from rest_framework import viewsets
from rest_auth.registration.views import RegisterView as BaseRegisterView

from accounts.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(BaseRegisterView):

    def perform_create(self, serializer):
        user = super().perform_create(serializer)

        if settings.CLEARBIT_KEY:
            try:
                clearbit.key = settings.CLEARBIT_KEY
                clearbit_info = clearbit.Person.find(email=user.email)
                user.clearbit_info = clearbit_info
                user.save()
            except HTTPError:
                pass

        return user
