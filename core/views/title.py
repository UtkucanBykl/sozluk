from django.db.models import Count, Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import TitleSerializer, CategorySerializer
from ..permissions import IsOwnerOrReadOnly
from ..models import Title, Category
from ..filters import TitleFilter

__all__ = ['TitleRetrieveUpdateDestroyAPIView', 'TitleListCreateAPIView', 'CategoryListAPIView']


class TitleRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TitleSerializer
    queryset = Title.objects.actives()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.today_entry_counts().total_entry_counts()


class TitleListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    queryset = Title.objects.actives().select_related('category')
    search_fields = ['title']
    order_fields = ['created_at']
    filterset_class = TitleFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.today_entry_counts().total_entry_counts()


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.actives()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(title_count=Count('title', filter=Q(title__status='publish'), distinct=True))

