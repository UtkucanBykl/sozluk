from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions

from ..models import Entry, Like, Dislike
from ..pagination import StandardEntryPagination
from ..serializers import EntrySerializer
from ..filters import EntryFilter
from ..permissions import IsOwnerOrReadOnly, OwnModelPermission


__all__ = ['EntryListCreateAPIView', 'EntryRetrieveUpdateDestroyAPIView']


class EntryListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EntrySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['title']
    ordering_fields = ['like_count', 'dislike_count', 'created_at']
    filterset_class = EntryFilter
    pagination_class = StandardEntryPagination

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            qs = Entry.objects.deletes_or_actives()
        else:
            qs = Entry.objects.filter()

        if self.request.query_params.get('status') and self.request.user.is_authenticated:
            qs = qs.filter(status=self.request.query_params.get('status'), user=self.request.user)
        else:
            qs = qs.actives()
        likes_prefetch = Prefetch('likes', Like.objects.select_related('user').filter())
        dislikes_prefetch = Prefetch('dislikes', Dislike.objects.select_related('user').filter())

        return qs.is_user_like(self.request.user).is_user_dislike(
            self.request.user).count_like_and_dislike().get_without_block_user(self.request.user).select_related(
            'title').prefetch_related(
            likes_prefetch, dislikes_prefetch)

    def perform_create(self, serializer):
        serializer.user = self.request.user
        serializer.save()


class EntryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [OwnModelPermission|IsOwnerOrReadOnly]
    authentication_classes = (TokenAuthentication,)
    serializer_class = EntrySerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = Entry.objects.actives()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.is_user_like(self.request.user).get_without_block_user(self.request.user).select_related('title')

    def perform_destroy(self, instance):
        instance.delete(user=self.request.user)
