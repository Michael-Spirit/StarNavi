from django.conf import settings
from django.db.models import Model, CharField, TextField, ForeignKey, CASCADE, SmallIntegerField, Manager, Sum


class VoteManager(Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0).count()

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0).count()

    def sum_rating(self, post):
        return self.get_queryset().filter(post=post).aggregate(Sum('vote')).get('vote__sum') or 0


class Post(Model):
    title = CharField(max_length=120, null=False, blank=False)
    text = TextField(null=False, blank=False)
    author = ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=CASCADE)

    @property
    def rating(self):
        return Vote.objects.sum_rating(post=self)


class Vote(Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = SmallIntegerField(verbose_name="vote", choices=VOTES)
    post = ForeignKey(Post, blank=False, null=False, on_delete=CASCADE)
    author = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    objects = VoteManager()
