from django.db.models import Prefetch, Q
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions

from ..models import Entry, Like, Dislike, Favorite, Title
from ..pagination import StandardEntryPagination
from ..serializers import EntrySerializer, EntryUpdateSerializer
from ..filters import EntryFilter
from ..permissions import IsOwnerOrReadOnly, OwnModelPermission
from ..tasks import create_notification_entry_create_info_to_title_user

import random

__all__ = ['EntryListCreateAPIView', 'EntryRetrieveUpdateDestroyAPIView']


class EntryListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EntrySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['title']
    ordering_fields = ['like_count', 'dislike_count', 'favorite_count', 'created_at']
    filterset_class = EntryFilter
    pagination_class = StandardEntryPagination

    def get_queryset(self):
        if self.request.query_params.get('status') and self.request.user.is_authenticated:
            qs = Entry.objects.filter(status=self.request.query_params.get('status'), user=self.request.user)
        elif self.request.user.is_authenticated and self.request.user.is_staff:
            qs = Entry.objects.filter(Q(status='publish') | Q(status='deleted') | Q(status="publish_by_rookie"))
        elif self.request.query_params.get('user_id'):
            qs = Entry.objects.filter(user_id=self.request.query_params.get('user_id'), status='publish')
        elif self.request.query_params.get('random'):
            id_list = Entry.objects.all().values_list('id', flat=True)
            random_profiles_id_list = random.sample(list(id_list), min(len(id_list), 33))
            qs = Entry.objects.filter(id__in=random_profiles_id_list)
        else:
            qs = Entry.objects.actives()

        return qs.is_user_like(self.request.user).is_user_dislike(
            self.request.user).is_user_favorite(self.request.user).count_like_and_dislike_and_favorite(). \
            get_without_block_user(self.request.user).select_related('title')

    def perform_create(self, serializer):
        serializer.user = self.request.user
        if self.request.data['title']:
            title = Title.objects.get(id=self.request.data['title'])
            if title and title.user:
                if self.request.user.pk != title.user.pk:
                    create_notification_entry_create_info_to_title_user.send(self.request.user.pk, title.title, title.user.username)
        serializer.save()


class EntryRetrieveUpdateDestroyAPIView(DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [OwnModelPermission | IsOwnerOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    serializer_class = EntrySerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Entry.objects.actives()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "retrieve":
            return qs.is_user_like(self.request.user).get_without_block_user(self.request.user).select_related('title')
        return qs

    def perform_destroy(self, instance):
        instance.delete(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return EntryUpdateSerializer
        else:
            return EntrySerializer
