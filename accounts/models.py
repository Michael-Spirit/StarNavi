from django.contrib.auth.models import AbstractUser as BaseUser
from django.contrib.postgres.fields import JSONField


class User(BaseUser):
    clearbit_info = JSONField(default=dict)
