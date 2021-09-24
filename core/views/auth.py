from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User

from django.utils import timezone

from ..serializers import RegisterSerializer, LoginSerializer

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
        user = User.objects.filter(username=request.data['username']).first()
        today = timezone.now().date()
        if user.punish_finish_date and today < user.punish_finish_date:
            return Response({'error_message': str(user.punish_finish_date) + ' tarihine kadar cezalısınız.'})
        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.login(request.data)
            return Response(data, status=status.HTTP_200_OK)
