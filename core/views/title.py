from django.db.models import Count, Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend


from ..pagination import StandardTitlePagination
from ..serializers import TitleSerializer, CategorySerializer, NotShowTitleSerializer

from ..permissions import IsOwnerOrReadOnly
from ..models import Title, Category, NotShowTitle
from ..filters import TitleFilter

from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

__all__ = ['TitleRetrieveUpdateDestroyAPIView', 'TitleListCreateAPIView', 'CategoryListAPIView', 'NotShowTitleCreateAPIView']


class TitleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TitleSerializer
    queryset = Title.objects.actives()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.today_entry_counts().total_entry_counts().get_titles_without_not_showing(self.request.user)


class TitleListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    queryset = Title.objects.actives().select_related('category')
    search_fields = ['title']
    order_fields = ['created_at', 'total_entry_count', 'today_entry_count']
    filterset_class = TitleFilter
    pagination_class = StandardTitlePagination

    def get_permissions(self):
        if self.request.method == "post":
            self.permission_classes = (TokenAuthentication,)
        else:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.today_entry_counts().total_entry_counts().get_titles_without_not_showing(self.request.user)


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.actives()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(title_count=Count('title', filter=Q(title__status='publish'), distinct=True))


class NotShowTitleCreateAPIView(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = NotShowTitleSerializer
    permission_classes = (IsAuthenticated&IsOwnerOrReadOnly,)
    lookup_field = "title_id"
    lookup_url_kwarg = "title_id"

    def get_queryset(self):
        return NotShowTitle.objects.filter(user=self.request.user).actives()
