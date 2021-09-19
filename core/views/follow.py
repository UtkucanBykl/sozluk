from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

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

    def perform_destroy(self, instance):
        instance.delete(hard=True)


class UserFollowListCreateAPIView(ListCreateAPIView):
    serializer_class = UserFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        if self.request.query_params.get('query') == "following_users":
            return UserFollow.objects.filter(follower_user=self.request.user).actives().select_related('following_user')
        return UserFollow.objects.filter(following_user=self.request.user).actives().select_related('follower_user')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_following = UserFollow.objects.filter(follower_user=self.request.user.pk, following_user=self.request.data['following_user'])
        if is_following.exists():
            return Response({"error_message": "Bu kullanıcıyı zaten takip ediyorsunuz."})
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
