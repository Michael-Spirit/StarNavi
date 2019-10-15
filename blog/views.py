from rest_framework import viewsets

from blog.serializers import PostSerializer, VoteSerializer
from blog.models import Post, Vote

from rest_framework.response import Response
from rest_framework import status


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        any_vote = Vote.objects.filter(
            post=self.request.data['post'],
            author=self.request.data['author'])\
            .exists()
        same_vote = Vote.objects.filter(
            post=self.request.data['post'],
            vote=self.request.data['vote'],
            author=self.request.data['author'])\
            .exists()

        if any_vote and not same_vote:
            Vote.objects.filter(
                post=self.request.data['post'],
                author=self.request.data['author']).update(vote=self.request.data['vote'])
            return Response({'data': 'Vote changed'}, status=status.HTTP_200_OK)
        if any_vote and same_vote:
            Vote.objects.filter(
                post=self.request.data['post'],
                vote=self.request.data['vote'],
                author=self.request.data['author']).delete()
            return Response({'data': 'Vote removed'}, status=status.HTTP_202_ACCEPTED)

        return super().create(request, *args, **kwargs)
