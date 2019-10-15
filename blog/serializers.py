from rest_framework import serializers
from blog.models import Post, Vote


class PostSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    is_voted = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'pk', 'title', 'text', 'author', 'rating', 'is_voted')

    def get_is_voted(self, obj):
        user = self.context['request']._user

        if Vote.objects.filter(post=obj, author=user).exists():
            return Vote.objects.get(post=obj, author=user).vote

        return None


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
