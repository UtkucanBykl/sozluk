from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token

__all__ = ['UserSerializer']

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'id')
        model = Group


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'is_superuser', 'is_staff', 'first_name', 'last_name', 'token',
                  'groups')

    def get_token(self, obj):
        return Token.objects.filter(user=obj).first().key
