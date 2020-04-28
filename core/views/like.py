from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers import LikeSerializer
from ..models import Like

__all__ = ['LikeListCreateAPIView']


class LikeListCreateAPIView(ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).actives().select_related('entry', 'user')
