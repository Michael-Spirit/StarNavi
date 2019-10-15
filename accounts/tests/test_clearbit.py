import clearbit

from rest_framework.test import APITestCase


class TestClearbit(APITestCase):

    def test_email(self):
        clearbit.key = 'sk_11df5e32e7f953d02e89cb4b55ba756f'
        me = clearbit.Person.find(email='MSpiridonov94@gmail.com')
        self.assertEqual(me['name']['fullName'], "Mikhail Spiridonov")
