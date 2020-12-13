from django.contrib.auth import get_user_model

from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UserSerializer, UserUpdateSerializer, ChangePasswordSerializer


User = get_user_model()

__all__ = ["UserRetrieveUpdateViewSet", "ChangeUserPasswordView"]


class UserRetrieveUpdateViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_url_kwarg = "id"
    lookup_field = "id"

    def get_permissions(self):
        if self.action == "partial_update":
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def get_object(self):
        if self.action == "partial_update":
            return self.request.user
        else:
            return super().get_object()

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UserUpdateSerializer
        else:
            return UserSerializer


class ChangeUserPasswordView(views.APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = request.user
            user.set_password(request.data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
