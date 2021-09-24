from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserSerializer, UserUpdateSerializer, ChangePasswordSerializer, \
    UserBlockSerializer, UserBlockUpdateSerializer, UserEmotionSerializer, PunishUserSerializer
from ..models import Block


User = get_user_model()

__all__ = ["UserRetrieveUpdateViewSet", "ChangeUserPasswordView", "BlockUserViewSet", "UserSearchAPIView",
           "PunishUserAPIView"]


class UserRetrieveUpdateViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_url_kwarg = "id"
    lookup_field = "id"

    def get_permissions(self):
        if self.action == "partial_update":
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_object(self):
        if self.action == "partial_update":
            return self.request.user
        else:
            return super().get_object()

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UserUpdateSerializer
        else:
            return UserSerializer


class ChangeUserPasswordView(views.APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = request.user
            user.set_password(request.data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class BlockUserViewSet(DestroyModelMixin, UpdateModelMixin, CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = UserBlockSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = "blocked_user"
    lookup_url_kwarg = "blocked_user_id"

    def get_queryset(self):
        return Block.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UserBlockUpdateSerializer
        return UserBlockSerializer


class UserSearchAPIView(ListModelMixin, GenericViewSet):
    serializer_class = UserEmotionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ['username']

    def get_queryset(self):
        if self.request.query_params.get('search'):
            qs = User.objects.all()
            return qs
        else:
            return User.objects.none()


class PunishUserAPIView(UpdateModelMixin, GenericViewSet):
    serializer_class = PunishUserSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    http_method_names = ['patch']
    lookup_url_kwarg = "id"
    lookup_field = "id"

    def get_queryset(self):
        return User.objects.get(id=self.kwargs.get(self.lookup_field))

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response({'error_message': 'Bu işlemi yapmaya yetkiniz yok.'})
