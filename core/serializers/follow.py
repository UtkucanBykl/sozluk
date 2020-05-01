from rest_framework import serializers

from ..serializers import TitleSerializer
from ..models import TitleFollow

__all__ = ['TitleFollowSerializer']


class TitleFollowSerializer(serializers.ModelSerializer):
    title_detail = TitleSerializer(source='entry', read_only=True, many=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TitleFollow
        fields = ('title', 'created_at', 'title_detail', 'user')
