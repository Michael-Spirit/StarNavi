import factory

from factory.fuzzy import FuzzyChoice
from blog.models import Post, Vote
from accounts.tests.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: 'title %s' % n)
    text = 'lorem ipsum and blah blah blah'
    author = factory.SubFactory(UserFactory)


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    vote = FuzzyChoice([-1, 1])
