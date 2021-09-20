from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..serializers import DislikeSerializer, LikeSerializer, FavoriteSerializer, EntryLikeSerializer, \
    EntryDislikeSerializer, EntryFavoriteSerializer
from ..models import Dislike, Like, Favorite, Entry
from ..pagination import StandardPagination
from ..tasks import decrement_like_dislike_favorite, increment_like_dislike_favorite, \
    create_notification_like, update_user_points, create_notification_dislike, create_notification_favorite

from rest_framework.response import Response
from rest_framework import status

from django.db import transaction
from django.utils import timezone

__all__ = ['LikeListCreateAPIView', 'DislikeListCreateAPIView', 'DeleteDislikeAPIView', 'DeleteLikeAPIView',
           'FavoriteListCreateAPIView', 'DeleteFavoriteAPIView']


class LikeListCreateAPIView(ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardPagination
    ordering_fields = ['created_at']
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
        try:
            entry = Entry.objects.get(id=self.request.data['entry'])
        except Exception as err:
            return Response({'error_message': 'Böyle bir entry yok.'})
        if entry:
            like = Like.objects.filter(user_id=self.request.user.pk, entry_id=entry.pk)
            if like.exists():
                return Response({'error_message': 'Bu içeriği zaten beğendiniz.'}, status=status.HTTP_200_OK)
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                create_notification_like.send(self.request.user.pk, entry.pk)
                update_user_points.send(entry.pk, 1)
                increment_like_dislike_favorite.send("like", entry.pk)

                with transaction.atomic():
                    entry.last_vote_time = timezone.now()
                    entry.save()

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        decrement_like_dislike_favorite.send("like", self.kwargs.get(self.lookup_field))
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteDislikeAPIView(DestroyAPIView):
    serializer_class = DislikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['delete']
    lookup_field = 'entry_id'

    def get_queryset(self):
        return Dislike.objects.filter(user=self.request.user).select_related('entry', 'user')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        decrement_like_dislike_favorite.send("dislike", self.kwargs.get(self.lookup_field))
        return Response(status=status.HTTP_204_NO_CONTENT)


class DislikeListCreateAPIView(ListCreateAPIView):
    serializer_class = DislikeSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardPagination
    ordering_fields = ['created_at']
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
        try:
            entry = Entry.objects.get(id=self.request.data['entry'])
        except Exception as err:
            return Response({'error_message': 'Böyle bir entry yok.'})
        if entry:
            dislike = Dislike.objects.filter(user_id=self.request.user.pk, entry_id=entry.pk)
            if dislike.exists():
                return Response({'error_message': 'Zaten bu içeriği beğenmediniz.'}, status=status.HTTP_200_OK)
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                create_notification_dislike.send(self.request.user.pk, entry.pk)
                update_user_points.send(entry.pk, -1)
                increment_like_dislike_favorite.send("dislike", entry.pk)

                with transaction.atomic():
                    entry.last_vote_time = timezone.now()
                    entry.save()
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FavoriteListCreateAPIView(ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardPagination
    ordering_fields = ['created_at']
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
        try:
            entry = Entry.objects.get(id=self.request.data['entry'])
        except Exception as err:
            return Response({'error_message': 'Böyle bir entry yok.'})
        if entry:
            favorite = Favorite.objects.filter(user_id=self.request.user.pk, entry_id=entry.pk)
            if favorite.exists():
                return Response({'error_message': 'Zaten bu içeriği favorilediniz.'})
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                create_notification_favorite(self.request.user.pk, entry.pk)
                update_user_points.send(entry.pk, 3)
                increment_like_dislike_favorite.send("favorite", entry.pk)

                with transaction.atomic():
                    entry.last_vote_time = timezone.now()
                    entry.save()
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        decrement_like_dislike_favorite.send("favorite", self.kwargs.get(self.lookup_field))
        return Response(status=status.HTTP_204_NO_CONTENT)