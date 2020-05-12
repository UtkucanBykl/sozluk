from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter

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


class TitleListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    queryset = Title.objects.actives()
    search_fields = ['title']
    filterset_class = TitleFilter

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET.get('today'):
            qs = qs.active_today()
        if self.request.GET.get('full_text'):
            qs = qs.full_text_search(self.request.GET.get('full_text'))
        return qs


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.actives()

