from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..serializers import FollowSerializer
from ..models import Follow

__all__ = ['FollowListCreateAPIView']


class FollowListCreateAPIView(ListCreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user).actives().select_related('entry', 'user')
