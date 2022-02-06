from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.postgres.search import TrigramSimilarity

from django_filters.rest_framework import DjangoFilterBackend
from ..pagination import StandardTitlePagination, StandardPagination
from ..serializers import TitleSerializer, NotShowTitleSerializer, EntrySerializer

from ..permissions import IsOwnerOrReadOnly
from ..models import Title, NotShowTitle, User, Entry
from ..filters import TitleFilter
from ..tasks import update_user_points_follow_or_title_create, update_user_points, \
    create_notification_title_with_username, combine_two_titles, change_tematik_entries_in_title

from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework import status
from rest_framework.response import Response

import random
import ast

__all__ = ['TitleUpdateDestroyAPIView', 'TitleListCreateAPIView',
           'NotShowTitleCreateAPIView', 'TitleWithEntryCreateAPIView', 'SimilarTitleListAPIView',
           'CombineTwoTitles', 'ChangeAllTematikEntriesInTitle']


class TitleUpdateDestroyAPIView(UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TitleSerializer
    queryset = Title.objects.actives()
    lookup_field = 'id'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.today_entry_counts().total_entry_counts().get_titles_without_not_showing(self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.request.user.is_superuser or (self.request.user == instance.user):
            # TODO: Buraya eğer superuser silme işlemini yaptıysa title sahibine notification verilmesi gerekir.
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error_message": "Bu başlığı silmeye yetkiniz yok."})


class TitleListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    queryset = Title.objects.actives()
    search_fields = ['title']
    ordering_fields = ['created_at', 'total_entry_count', 'today_entry_count']
    filterset_class = TitleFilter
    pagination_class = StandardTitlePagination

    def get_permissions(self):
        if self.request.method.lower() == "post":
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.user = self.request.user
        serializer.save()
        if hasattr(self.request.user, 'id'):
            update_user_points_follow_or_title_create.send(self.request.user.id, 5)

        title = self.request.data['title']
        is_username = User.objects.filter(username=title).first()

        if is_username and hasattr(is_username, 'id'):
            create_notification_title_with_username.send(self.request.user.id, title, is_username.id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.query_params.get('last24hour'):
            return qs.active_today_created_date()
        elif self.request.query_params.get('random'):
            id_list = Title.objects.filter(status='publish').all().values_list('id', flat=True)
            random_profiles_id_list = random.sample(list(id_list), min(len(id_list), 33))
            qs = Title.objects.filter(id__in=random_profiles_id_list)
            return qs.get_titles_without_not_showing(self.request.user)
        elif self.request.query_params.get('user_id') and self.request.query_params.get('is_ukde'):
            qs = Title.objects.filter(
                user=self.request.query_params.get('user_id'), is_ukde=self.request.query_params.get('is_ukde')
            )
            return qs.get_titles_without_not_showing(self.request.user)
        return qs.get_titles_without_not_showing(self.request.user)


class TitleWithEntryCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

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
        qs = Title.objects.annotate(similarity=TrigramSimilarity('title', title), ) \
            .filter(similarity__gt=0.1).order_by('-similarity')
        return qs


class CombineTwoTitles(CreateModelMixin, GenericViewSet):
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def create(self, request, *args, **kwargs):
        # TODO: Buraya hem from_title'ın sahibi hemde to_title'ın sahibine notification verilmesi gerekir.
        if self.request.user.is_superuser or self.request.user.account_type == 'mod':
            combine_two_titles.send(self.request.data['from_title'], self.request.data['to_title'],
                                    self.request.user.pk)
            return Response({"system_message": "Başlıkları birleştirme işlemi başlatıldı."})
        else:
            return Response({"error_message": "Bu işlemi yapmak için yetkiniz yok."})


class ChangeAllTematikEntriesInTitle(CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.account_type == 'mod':
            change_tematik_entries_in_title.send(self.kwargs.get('id'), self.request.user.pk)
            return Response({"system_message": "Tematik tanımları normale çevirme işlemi başlatıldı."})
        else:
            return Response({"error_message": "Bu işlemi yapmak için yetkiniz yok."})