from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from accounts.tests.factories import UserFactory, TEST_USER_PASSWORD
from allauth.account.models import EmailAddress


class TestAuth(APITestCase):

    def test_registration(self):
        data = {
            'email': 'test@mail.com',
            'password1': 'test-password123',
            'password2': 'test-password123'
        }

        response = self.client.post(reverse('rest_register'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_login_success(self):
        user = UserFactory()
        data = {
            'email': user.email,
            'password': TEST_USER_PASSWORD
        }

        response = self.client.post(reverse('rest_login'), data=data)
        self.assertIsNotNone(response.data['token'])

    def test_login_unverified_email(self):
        user = UserFactory()
        EmailAddress.objects.filter(email=user.email).update(verified=False)

        data = {
            'email': user.email,
            'password': TEST_USER_PASSWORD
        }

        response = self.client.post(reverse('rest_login'), data=data)
        self.assertContains(response, data['email'], status_code=200)
