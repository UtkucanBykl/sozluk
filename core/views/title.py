from django.db.models import Count, Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.postgres.search import TrigramSimilarity

from django_filters.rest_framework import DjangoFilterBackend

from ..pagination import StandardTitlePagination, StandardPagination
from ..serializers import TitleSerializer, CategorySerializer, NotShowTitleSerializer, EntrySerializer

from ..permissions import IsOwnerOrReadOnly
from ..models import Title, Category, NotShowTitle, User
from ..filters import TitleFilter
from ..tasks import update_user_points_follow_or_title_create, update_user_points

from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework import status
from rest_framework.response import Response

import random
import ast

__all__ = ['TitleRetrieveUpdateDestroyAPIView', 'TitleListCreateAPIView', 'CategoryListAPIView',
           'NotShowTitleCreateAPIView', 'TitleWithEntryCreateAPIView', 'SimilarTitleListAPIView']


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
        if self.request.method.lower() == "post":
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('random'):
            id_list = Title.objects.all().values_list('id', flat=True)
            random_profiles_id_list = random.sample(list(id_list), min(len(id_list), 33))
            qs = Title.objects.filter(id__in=random_profiles_id_list)
            return qs
        return qs.today_entry_counts().total_entry_counts().get_titles_without_not_showing(self.request.user)


class TitleWithEntryCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):
        title_data = self.request.data.get('title', {})
        title_serializer = TitleSerializer(data=ast.literal_eval(title_data), context=self.get_serializer_context())
        if title_serializer.is_valid(raise_exception=True):
            title = title_serializer.save()
            update_user_points_follow_or_title_create.send(self.request.user.id, 5)
            entry_data = ast.literal_eval(self.request.data.get('entry'))
            entry_data['title'] = title.id
            entry_serializer = EntrySerializer(data=entry_data, context=self.get_serializer_context())
            if entry_serializer.is_valid(raise_exception=True):
                entry = entry_serializer.save()
                update_user_points.send(entry.id, 2)
                title.is_ukde = False
                title_serializer.save(data=title)
                return Response(status=status.HTTP_201_CREATED)


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.actives()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(title_count=Count('title', filter=Q(title__status='publish'), distinct=True))


class NotShowTitleCreateAPIView(DestroyModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = NotShowTitleSerializer
    permission_classes = (IsAuthenticated & IsOwnerOrReadOnly,)
    lookup_field = "title_id"
    lookup_url_kwarg = "title_id"

    def get_queryset(self):
        return NotShowTitle.objects.filter(user=self.request.user).actives()


class SimilarTitleListAPIView(ListAPIView):
    serializer_class = TitleSerializer
    pagination_class = StandardPagination
    permission_classes = (AllowAny,)

    def get_queryset(self):
        title = self.request.query_params.get('title')
        qs = Title.objects.annotate(similarity=TrigramSimilarity('title', title),)\
            .filter(similarity__gt=0.1).order_by('-similarity')
        return qs
