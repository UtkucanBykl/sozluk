from rest_framework import serializers

from ..models import Title

__all__ = ['TitleSerializer']


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('title', 'updated_at', 'is_bold', 'can_write', 'category')
