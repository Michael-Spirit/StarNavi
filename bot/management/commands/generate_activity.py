import random
import json

from factory.fuzzy import FuzzyInteger

from django.core.management.base import BaseCommand
from django.conf import settings

from blog.tests.factories import PostFactory, VoteFactory
from accounts.tests.factories import UserFactory
from bot.utils import generate_random_email


class Command(BaseCommand):
    help = "Generate user, posts and likes in system"

    def handle(self, *args, **options):
        users = []
        posts = []
        votes = []

        with open(settings.BASE_DIR + '/bot-config.json') as config:
            config = json.load(config)

        for x in range(config['number_of_users']):
            user = UserFactory(email=generate_random_email())
            users.append(user)

        for user in users:
            random_posts = FuzzyInteger(0, config['max_posts_per_user']).fuzz()
            print('Random posts for User ({}) -> {}'.format(user.username, random_posts))
            for _ in range(random_posts):
                posts.append(PostFactory(author=user))

        for user in users:
            random_votes = FuzzyInteger(0, config['max_votes_per_user']).fuzz()
            print('Random votes for User ({}) -> {}'.format(user.username, random_votes))
            for _ in range(random_votes):
                votes.append(VoteFactory(author=user, post=random.choice(posts)))
