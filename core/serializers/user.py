from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

from ..models import Block, Title, Entry, UserFollow


__all__ = ['UserSerializer', 'LoginUserSerializer', 'UserUpdateSerializer', 'ChangePasswordSerializer',
           "UserBlockSerializer", "UserBlockUpdateSerializer", "UserEmotionSerializer", "UserMessageSerializer"]

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
        fields = ('id', 'username', 'email', 'is_active', 'bio', 'account_type',
                  'is_superuser', 'is_staff', 'first_name', 'last_name', 'token',
                  'groups', 'profile_picture', 'account_type', 'point', 'created_at')

    def get_token(self, obj):
        return Token.objects.filter(user=obj).first().key


class UserSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()
    title_count = serializers.SerializerMethodField()
    entry_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'is_superuser', 'is_staff', 'first_name', 'last_name',
                  'profile_picture', 'city', 'is_show_city', 'birth_day', 'is_show_birth_day', 'gender',
                  'is_show_gender', 'twitter_username', 'facebook_profile', 'account_type', 'point',
                  'created_at', 'title_count', 'entry_count', 'follower_count')

    def get_title_count(self, user):
        title_count = Title.objects.filter(user=user).count()
        return title_count

    def get_entry_count(self, user):
        entry_count = Entry.objects.filter(user=user, status='publish').count()
        return entry_count

    def get_follower_count(self, user):
        follower_user = UserFollow.objects.filter(following_user=user).count()
        return follower_user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.show_bio or self.context.get("request").user == instance:
            data["show_bio"] = instance.show_bio
        else:
            data["bio"] = ""
        return data

class UserEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('bio', 'first_name', 'last_name', 'profile_picture', 'city', 'is_show_city', 'birth_day',
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


class UserBlockSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Block
        fields = ('user', 'blocked_user', "is_message", "is_entry")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["blocked_user"] = UserSerializer(instance.blocked_user, many=False).data
        return data

    def validate(self, attrs):
        blocked_user = attrs.get("blocked_user")
        if blocked_user.id == self.context.get("request").user.id:
            raise serializers.ValidationError("Kendini engelleyemezsin.")
        return attrs


class UserBlockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ("is_message", "is_entry")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["blocked_user"] = UserSerializer(instance.blocked_user, many=False).data
        return data


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'profile_picture', 'username')
