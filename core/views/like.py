from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

<<<<<<< Updated upstream
from ..serializers import LikeSerializer
from ..models import Like
from ..tasks import create_notification_like
=======
from ..serializers import DislikeSerializer, LikeSerializer
from ..models import Dislike, Like
>>>>>>> Stashed changes

__all__ = ['LikeListCreateAPIView', 'DislikeListCreateAPIView']


class LikeListCreateAPIView(ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post', 'put', 'get', 'delete']

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user).actives().select_related('entry', 'user')

<<<<<<< Updated upstream
    def create(self, request, *args, **kwargs):
        create = super().create(request, *args, **kwargs)
        create_notification_like.send(from_user_id=self.request.user.id, entry_id=request.data.get('entry'))
        return create

=======

class DislikeListCreateAPIView(ListCreateAPIView):
    serializer_class = DislikeSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post', 'put', 'get', 'delete']

    def get_queryset(self):
        return Dislike.objects.filter(user=self.request.user).actives().select_related('entry', 'user')
>>>>>>> Stashed changes
