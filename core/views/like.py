from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers import DislikeSerializer, LikeSerializer
from ..models import Dislike, Like


__all__ = ['LikeListCreateAPIView', 'DislikeListCreateAPIView', 'DeleteDislikeAPIView', 'DeleteLikeAPIView']


class LikeListCreateAPIView(ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post', 'get', 'delete']

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related('entry', 'user')


class DeleteLikeAPIView(DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['delete']
    lookup_field = 'entry_id'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related('entry', 'user')


class DeleteDislikeAPIView(DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['delete']
    lookup_field = 'entry_id'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related('entry', 'user')


class DislikeListCreateAPIView(ListCreateAPIView):
    serializer_class = DislikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post', 'get', 'delete']
    lookup_field = 'entry_id'

    def get_queryset(self):
        return Dislike.objects.filter(user=self.request.user).select_related('entry', 'user')
