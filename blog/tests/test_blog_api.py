from rest_framework.test import APITestCase

from rest_framework.reverse import reverse
from accounts.tests.factories import UserFactory, TEST_USER_PASSWORD
from blog.tests.factories import PostFactory
from blog.models import Post, Vote


class TestBlogBasics(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        data = {
            'email': self.user.email,
            'password': TEST_USER_PASSWORD
        }

        self.client.post(reverse('rest_login'), data=data)

    def test_blog_CRUD(self):
        # Create
        data = {
            'title': 'Title Test',
            'text': 'test text',
            'author': self.user.id
        }

        self.client.post(reverse('post-list'), data=data)
        post = Post.objects.first()
        self.assertEqual(post.title, data['title'])

        # Retrieve
        response = self.client.get(reverse('post-detail', kwargs={'pk': post.id}))
        self.assertEqual(response.data['id'], post.id)
        self.assertEqual(response.data['title'], post.title)

        # Update
        update_data = {'title': 'Title 2'}
        self.client.patch(reverse('post-detail', kwargs={'pk': post.id}), data=update_data)
        updated_post = Post.objects.first()
        self.assertEqual(updated_post.title, update_data['title'])

        # Delete
        self.client.delete(reverse('post-detail', kwargs={'pk': post.id}))
        self.assertEqual(Post.objects.count(), 0)

    def test_blog_perms(self):
        self.client.logout()
        data = {
            'title': 'Title Test',
            'text': 'test text',
            'author': self.user.id
        }

        response = self.client.post(reverse('post-list'), data=data)
        self.assertContains(response, "Authentication credentials were not provided.", status_code=401)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_vote_CRUD(self):
        post = PostFactory(author=self.user)

        # Create
        data = {
            'author': self.user.id,
            'post': post.id,
            'vote': 1
        }
        self.client.post(reverse('vote-list'), data=data)
        vote = Vote.objects.first()
        self.assertEqual(vote.vote, data['vote'])

        # Retrieve
        response = self.client.get(reverse('vote-detail', kwargs={'pk': vote.id}))
        self.assertEqual(response.data['id'], vote.id)
        self.assertEqual(response.data['post'], vote.post.id)

        # Update
        update_data = {'vote': -1}
        self.client.patch(reverse('vote-detail', kwargs={'pk': vote.id}), data=update_data)
        updated_vote = Vote.objects.first()
        self.assertEqual(updated_vote.vote, update_data['vote'])

        # Delete
        self.client.delete(reverse('vote-detail', kwargs={'pk': vote.id}))
        self.assertEqual(Vote.objects.count(), 0)
