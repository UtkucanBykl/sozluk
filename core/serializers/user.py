from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

__all__ = ['UserSerializer', 'LoginUserSerializer', 'UserUpdateSerializer', 'ChangePasswordSerializer']

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
        fields = ("id", 'username', 'email', 'is_active', 'bio', 'is_superuser', 'is_staff', 'first_name', 'last_name', 'token',
                  'groups', 'profile_picture', "account_type")

    def get_token(self, obj):
        return Token.objects.filter(user=obj).first().key


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", 'username', 'email', 'bio', 'is_superuser', 'is_staff', 'first_name', 'last_name', 'profile_picture', 'city',
                  'is_show_city', 'birth_day', 'is_show_birth_day', 'gender', 'is_show_gender', 'twitter_username',
                  'facebook_profile', 'account_type')

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
        fields = ("bio", 'first_name', 'last_name', 'profile_picture', 'city', 'is_show_city', 'birth_day',
                  'is_show_birth_day', 'gender', 'is_show_gender', 'twitter_username', 'facebook_profile')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = ("old_password", "new_password")

    def validated_old_password(self, old_password):
        request = self.context.get("request")
        user = request.user
        valid_password = user.check_password(old_password)
        if not valid_password:
            raise ValidationError("Current password is wrong!")
        return old_password
