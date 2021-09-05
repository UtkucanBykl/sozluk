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
    queryset = UserEmotionActivities.objects.actives()
