from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from ..pagination import StandardPagination
from ..models import UserEmotionActivities
from ..serializers import UserEmotionLastActivitiesGet


__all__ = ['UserEmotionActivitiesAPIView']


class UserEmotionActivitiesAPIView(ListModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = StandardPagination
    serializer_class = UserEmotionLastActivitiesGet
    http_method_names = ['get']

    def get_queryset(self):
        if self.request.query_params.get('user_id'):
            qs = UserEmotionActivities.objects.filter(user=self.request.query_params.get('user_id')).order_by('-created_at')
            return qs.actives()
        return UserEmotionActivities.objects.none()
