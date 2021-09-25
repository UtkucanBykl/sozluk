from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import PunishSerializer
from ..mixins import OwnerOrReadOnlyMixin
from ..models import User, PunishUser

__all__ = ['PunishListCreateAPIView']


class PunishListCreateAPIView(OwnerOrReadOnlyMixin, ListCreateAPIView):
    serializer_class = PunishSerializer
    authentication_classes = (TokenAuthentication,)
    http_method_names = ["post", "get"]

    def get_queryset(self):
        return PunishUser.objects.filter(punished_user=self.request.user)

    def create(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.account_type == 'mod':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error_message': 'Bu işlemi yapmak için yetkiniz yok.'})