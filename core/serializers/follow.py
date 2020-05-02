from rest_framework import serializers

from ..serializers import TitleSerializer, UserSerializer
from ..models import TitleFollow, UserFollow

__all__ = ['TitleFollowSerializer', 'UserFollowSerializer']


class TitleFollowSerializer(serializers.ModelSerializer):
    title_detail = TitleSerializer(source='title', read_only=True, many=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TitleFollow
        fields = ('title', 'created_at', 'title_detail', 'user')


class UserFollowSerializer(serializers.ModelSerializer):
    following_user_detail = UserSerializer(source='following_user', read_only=True, many=False)
    follower_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFollow
        fields = ('following_user', 'created_at', 'following_user_detail', 'follower_user')