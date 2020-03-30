from rest_framework import serializers

from ..serializers import TitleSerializer
from ..models import Follow

__all__ = ['FollowSerializer']


class FollowSerializer(serializers.ModelSerializer):
    title_detail = TitleSerializer(source='entry', read_only=True, many=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('title', 'created_at', 'title_detail', 'user')
