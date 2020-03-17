from rest_framework import serializers

from ..serializers import EntrySerializer
from ..models import Follow

__all__ = ['FollowSerializer']


class FollowSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', read_only=True, many=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ('entry', 'created_at', 'entry_detail', 'user')
