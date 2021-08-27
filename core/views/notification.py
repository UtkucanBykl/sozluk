from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..serializers import NotificationSerializer, NotificationGetSerializer
from ..pagination import StandardPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, ListModelMixin

from ..models import Notification

__all__ = ['NotificationListAPIView']


class NotificationListAPIView(ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardPagination
    lookup_url_kwarg = "id"
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action == "list":
            return NotificationGetSerializer
        else:
            return NotificationSerializer

    def get_queryset(self):
        qs = Notification.objects.filter(is_deleted=False, receiver_user=self.request.user)
        # return self.request.user.notifications.actives()
        return qs
