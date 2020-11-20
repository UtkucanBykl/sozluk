from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token

__all__ = ['UserSerializer', 'LoginUserSerializer', "UserUpdateSerializer"]

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'id')
        model = Group


class LoginUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'bio', 'is_superuser', 'is_staff', 'first_name', 'last_name', 'token',
                  'groups')

    def get_token(self, obj):
        return Token.objects.filter(user=obj).first().key


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'is_superuser', 'is_staff', 'first_name', 'last_name')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.show_bio or self.context.get("request").user == instance:
            data["show_bio"] = instance.show_bio
        else:
            data["bio"] = ""
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("bio", 'first_name', 'last_name')
