from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Entry
from ..serializers import EntrySerializer
from ..filters import EntryFilter
from ..permissions import IsOwnerOrReadOnly


__all__ = ['EntryListCreateAPIView', 'EntryRetrieveUpdateDestroyAPIView']


class EntryListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EntrySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    queryset = Entry.objects.actives()
    search_fields = ['title']
    filterset_class = EntryFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(title=self.kwargs.get('title_id')).is_user_like(
            self.request.user).count_like_and_dislike().select_related('title').prefetch_related('likes', 'dislikes')

    def perform_create(self, serializer):
        serializer.user = self.request.user
        serializer.save()


class EntryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = EntrySerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def get_queryset(self):
        return Entry.objects.actives().filter(id=self.kwargs.get('id')).is_user_like(self.request.user).select_related('title')
