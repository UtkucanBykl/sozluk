from rest_framework import serializers

from ..models import Like
from ..serializers import EntrySerializer

__all__ = ['LikeSerializer']


class LikeSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('entry', 'created_at', 'entry_detail', 'user')
