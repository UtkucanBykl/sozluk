from django.contrib.auth import get_user_model

from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet

from ..serializers import UserSerializer, UserUpdateSerializer


User = get_user_model()

__all__ = ["UserRetrieveUpdateViewSet"]


class UserRetrieveUpdateViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_url_kwarg = "id"
    lookup_field = "id"

    def get_permissions(self):
        if self.action == "update":
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_object(self):
        if self.action == "update":
            return self.request.user
        else:
            return super().get_object()

    def get_serializer_class(self):
        if self.action == "update":
            return UserUpdateSerializer
        else:
            return UserSerializer
