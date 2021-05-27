from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status

from ..serializers import MessageSerializer
from ..pagination import StandardPagination
from ..models import Message, User

from django.db.models import Q

__all__ = ['MessageListAPIView']


class MessageListAPIView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardPagination
    serializer_class = MessageSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.query_params.get('receiver_user'):
            second_user = User.objects.get(id=self.request.query_params.get('receiver_user'))
            qs = Message.objects.filter(Q(Q(sender_user=self.request.user) | Q(receiver_user=second_user)) |
                                        Q(Q(sender_user=second_user) | Q(receiver_user=self.request.user)))
            return qs
        return
