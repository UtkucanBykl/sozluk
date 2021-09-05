from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..serializers import DislikeSerializer, LikeSerializer, FavoriteSerializer, EntryLikeSerializer, EntryDislikeSerializer, EntryFavoriteSerializer
from ..models import Dislike, Like, Favorite, Entry, User, UserEmotionActivities
from ..pagination import StandardPagination

from rest_framework.response import Response
from rest_framework import status

__all__ = ['LikeListCreateAPIView', 'DislikeListCreateAPIView', 'DeleteDislikeAPIView', 'DeleteLikeAPIView',
           'FavoriteListCreateAPIView', 'DeleteFavoriteAPIView']


class LikeListCreateAPIView(ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardPagination
    http_method_names = ['post', 'get', 'delete']

    def get_queryset(self):
        if self.request.query_params.get('entry_id') and self.request.user.is_authenticated:
            return Like.objects.filter(entry_id=self.request.query_params.get('entry_id')).select_related('entry', 'user')
        elif self.request.query_params.get('user_id'):
            return Like.objects.filter(user_id=self.request.query_params.get('user_id')).select_related('entry', 'user')
        return Like.objects.filter(user=self.request.user).select_related('entry', 'user')

    def get_serializer_class(self):
        if self.request.query_params.get('entry_id') and self.request.user.is_authenticated:
            return EntryLikeSerializer
        return LikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        entry = Entry.objects.get(id=request.data['entry'])
        if entry:
            UserEmotionActivities.objects.create(user=self.request.user, entry=entry)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeleteLikeAPIView(DestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['delete']
    lookup_field = 'entry_id'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).select_related('entry', 'user')


class DeleteDislikeAPIView(DestroyAPIView):
    serializer_class = DislikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['delete']
    lookup_field = 'entry_id'

    def get_queryset(self):
        return Dislike.objects.filter(user=self.request.user).select_related('entry', 'user')


class DislikeListCreateAPIView(ListCreateAPIView):
    serializer_class = DislikeSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardPagination
    http_method_names = ['post', 'get', 'delete']
    lookup_field = 'entry_id'

    def get_queryset(self):
        if self.request.query_params.get('entry_id') and self.request.user.is_authenticated:
            return Dislike.objects.filter(entry_id=self.request.query_params.get('entry_id')).select_related('entry', 'user')
        elif self.request.query_params.get('user_id'):
            return Dislike.objects.filter(user_id=self.request.query_params.get('user_id')).select_related('entry', 'user')
        return Dislike.objects.filter(user=self.request.user).select_related('entry', 'user')

    def get_serializer_class(self):
        if self.request.query_params.get('entry_id') and self.request.user.is_authenticated:
            return EntryDislikeSerializer
        return DislikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        entry = Entry.objects.get(id=request.data['entry'])
        if entry:
            UserEmotionActivities.objects.create(user=self.request.user, entry=entry)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FavoriteListCreateAPIView(ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardPagination
    http_method_names = ['post', 'get']
    lookup_field = 'entry_id'

    def get_queryset(self):
        if self.request.query_params.get('entry_id') and self.request.user.is_authenticated:
            return Favorite.objects.filter(entry_id=self.request.query_params.get('entry_id')).select_related('entry', 'user')
        elif self.request.query_params.get('user_id'):
            return Favorite.objects.filter(user_id=self.request.query_params.get('user_id')).select_related('entry', 'user')
        return Favorite.objects.filter(user=self.request.user).select_related('entry', 'user')

    def get_serializer_class(self):
        if self.request.query_params.get('entry_id') and self.request.user.is_authenticated:
            return EntryFavoriteSerializer
        return FavoriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        entry = Entry.objects.get(id=request.data['entry'])
        if entry:
            UserEmotionActivities.objects.create(user=self.request.user, entry=entry)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeleteFavoriteAPIView(DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['delete']
    lookup_field = 'entry_id'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('entry', 'user')