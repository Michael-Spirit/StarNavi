import factory

from allauth.account.models import EmailAddress
from django.conf import settings

TEST_USER_PASSWORD = 'password'


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: 'user%s@example.com' % n)
    username = factory.Faker('name')
    password = factory.PostGenerationMethodCall('set_password', TEST_USER_PASSWORD)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_staff = False
    is_active = True

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('email',)

    @factory.post_generation
    def email_address(self, create, extracted, **kwargs):
        if create:
            EmailAddress.objects.create(user=self, email=self.email, verified=True, primary=True)


class AdminFactory(UserFactory):
    email = 'admin@admin.com'
    is_superuser = True
