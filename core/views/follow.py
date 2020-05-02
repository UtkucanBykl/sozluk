from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..serializers import TitleFollowSerializer, UserFollowSerializer
from ..models import TitleFollow, UserFollow

__all__ = ['TitleFollowListCreateAPIView', 'UserFollowListCreateAPIView']


class TitleFollowListCreateAPIView(ListCreateAPIView):
    serializer_class = TitleFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return TitleFollow.objects.filter(user=self.request.user).actives().select_related('entry', 'user')


class UserFollowListCreateAPIView(ListCreateAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return UserFollow.objects.filter(following_user=self.request.user).actives().select_related('follower_user')
