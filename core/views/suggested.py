from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import GenericViewSet

from ..models import Suggested
from ..serializers import SuggestedListSerializer, SuggestedCreateSerializer
from ..permissions import IsOwnerOrReadOnly


class SuggestedViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        CreateModelMixin,
        DestroyModelMixin,
        UpdateModelMixin,
        GenericViewSet
        ):

    queryset = Suggested.objects.actives()
    lookup_url_kwarg = "id"
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ("list", "retrieve", "create"):
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ("destroy", "update"):
            self.permission_classes = ((IsAuthenticated & IsOwnerOrReadOnly) | DjangoModelPermissions,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return SuggestedListSerializer
        elif self.action == "create":
            return SuggestedCreateSerializer
        elif self.action == "partial_update":
            return SuggestedCreateSerializer
        return SuggestedListSerializer
