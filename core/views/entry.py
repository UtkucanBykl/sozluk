from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions

from ..models import Entry, Like, Dislike
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

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            qs = Entry.objects.filter()
        else:
            qs = Entry.objects.actives()
        likes_prefetch = Prefetch('likes', Like.objects.select_related('user').filter())
        dislikes_prefetch = Prefetch('dislikes', Dislike.objects.select_related('user').filter())

        return qs.is_user_like(self.request.user).is_user_dislike(
            self.request.user).count_like_and_dislike().select_related(
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
        return qs.is_user_like(self.request.user).select_related('title')
