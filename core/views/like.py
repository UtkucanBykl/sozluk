from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..serializers import LikeSerializer
from ..models import Like

__all__ = ['LikeListCreateAPIView']


class LikeListCreateAPIView(ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    model = Like

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).actives()
