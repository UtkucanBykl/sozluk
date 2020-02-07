from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

__all__ = ['UserSerializer']

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'is_superuser', 'is_staff', 'first_name', 'last_name', 'token')

    def get_token(self, obj):
        return Token.objects.filter(user=obj).first().key
