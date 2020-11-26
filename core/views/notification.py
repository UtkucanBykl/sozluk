from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..serializers import NotificationSerializer
from ..pagination import  StandardPagination

__all__ = ['NotificationListAPIView']


class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']
    pagination_class = StandardPagination

    def get_queryset(self):
        return self.request.user.notifications.actives()
