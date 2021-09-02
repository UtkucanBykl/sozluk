from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..serializers import NotificationSerializer, NotificationGetSerializer
from ..pagination import StandardPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.response import Response

from ..tasks import seen_all_notification_for_user, delete_all_notification_for_user

from ..models import Notification
from rest_framework.filters import OrderingFilter


__all__ = ['NotificationListAPIView', 'NotificationDeleteAllAPIView', 'NotificationSeenAllAPIView']


class NotificationListAPIView(ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ['created_at']
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
        return qs


class NotificationDeleteAllAPIView(CreateModelMixin, GenericViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        delete_all_notification_for_user.send(self.request.user.pk)
        return Response({"system_info": "Tüm bildirimlerinin silme işlemi başlatılmıştır."})


class NotificationSeenAllAPIView(CreateModelMixin, GenericViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        seen_all_notification_for_user.send(self.request.user.pk)
        return Response({"system_info": "Tüm bildirimlerinin görüldü işlemi başlatılmıştır."})