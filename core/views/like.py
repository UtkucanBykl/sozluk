from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers import LikeSerializer
from ..models import Like
from ..tasks import create_notification_like

__all__ = ['LikeListCreateAPIView']


class LikeListCreateAPIView(ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).actives().select_related('entry', 'user')

    def create(self, request, *args, **kwargs):
        create = super().create(request, *args, **kwargs)
        create_notification_like.send(from_user_id=self.request.user.id, entry_id=request.data.get('entry'))
        return create

