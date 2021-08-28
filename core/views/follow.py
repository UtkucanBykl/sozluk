from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ..serializers import TitleFollowSerializer, UserFollowSerializer
from ..models import TitleFollow, UserFollow

__all__ = [
    'TitleFollowListCreateAPIView',
    'UserFollowListCreateAPIView',
    'UserFollowDeleteAPIView',
    'TitleFollowDeleteAPIView',
    'UserFollowRetrieveAPIView',
]


class TitleFollowListCreateAPIView(ListCreateAPIView):
    serializer_class = TitleFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return TitleFollow.objects.filter(user=self.request.user).actives().select_related('entry', 'user')


class TitleFollowDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'title_id'
    http_method_names = ['delete']

    def get_queryset(self):
        return self.request.user.follows.actives()


class UserFollowDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'following_user_id'
    http_method_names = ['delete']

    def get_queryset(self):
        return self.request.user.followings.actives()


class UserFollowListCreateAPIView(ListCreateAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        if self.request.query_params.get('query') == "following_users":
            return UserFollow.objects.filter(follower_user=self.request.user).actives().select_related('following_user')
        return UserFollow.objects.filter(following_user=self.request.user).actives().select_related('follower_user')


class UserFollowRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = UserFollow.objects.all()
    lookup_field = 'following_user_id'

    def retrieve(self, request, *args, **kwargs):
        is_following = UserFollow.objects.filter(follower_user=self.request.user.pk,
                                                 following_user=self.kwargs.get(self.lookup_field))
        if is_following:
            return Response({"is_following": True})
        else:
            return Response({"is_following": False})
