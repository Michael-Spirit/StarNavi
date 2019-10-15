import clearbit
from django.conf import settings

from accounts.models import User
from rest_framework import viewsets
from rest_auth.registration.views import RegisterView as BaseRegisterView

from accounts.serializers import UserSerializer

clearbit.key = settings.CLEARBIT_KEY


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(BaseRegisterView):

    def perform_create(self, serializer):
        user = super().perform_create(serializer)

        user.clearbit_info = clearbit.Person.find(email=user.email)
        user.save()

        return user
