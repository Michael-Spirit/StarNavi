import clearbit
from django.conf import settings

from rest_framework.test import APITestCase


class TestClearbit(APITestCase):

    def test_email(self):
        if not settings.CLEARBIT_KEY:
            print('For test clearbit you might add your clearbit key to local_settings.py')
            return
        clearbit.key = settings.CLEARBIT_KEY
        me = clearbit.Person.find(email='MSpiridonov94@gmail.com')
        self.assertEqual(me['name']['fullName'], "Mikhail Spiridonov")
