from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate


from django.utils import timezone

from ..serializers import RegisterSerializer, LoginSerializer, LoginUserSerializer
from ..models import PunishUser, User

__all__ = ['RegisterView', 'LoginView']


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    http_method_names = ['POST', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(request.data)
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = LoginSerializer
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=self.request.data.get('username'), password=self.request.data.get('password'))
        if user is not None:
            punished_user = PunishUser.objects.filter(punished_user=user.pk, status='publish').first()
            today = timezone.now().date()
            if punished_user and today < punished_user.punish_finish_date:
                return Response({'error_message': str(punished_user.punish_finish_date) + ' tarihine kadar cezalısınız.', "status_code": status.HTTP_401_UNAUTHORIZED})
            else:
                return Response({"user": LoginUserSerializer(user, many=False).data, "status_code": status.HTTP_200_OK})
        return Response({'error_message': 'Username or password incorrect', "status_code": status.HTTP_400_BAD_REQUEST})
