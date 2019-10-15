from django.core.management import call_command
from rest_framework.test import APITestCase

from blog.models import Post, Vote
from accounts.models import User


class TestBot(APITestCase):

    def test_bot_command(self):
        call_command('generate_activity')

        self.assertTrue(User.objects.all().exists())
        self.assertTrue(Post.objects.all().exists())
        self.assertTrue(Vote.objects.all().exists())

    def test_bot_command_twice(self):
        call_command('generate_activity')
        call_command('generate_activity')

        self.assertTrue(User.objects.all().exists())
        self.assertTrue(Post.objects.all().exists())
        self.assertTrue(Vote.objects.all().exists())
