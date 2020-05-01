from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..serializers import TitleFollowSerializer
from ..models import TitleFollow

__all__ = ['TitleFollowListCreateAPIView']


class TitleFollowListCreateAPIView(ListCreateAPIView):
    serializer_class = TitleFollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return TitleFollow.objects.filter(user=self.request.user).actives().select_related('entry', 'user')
