from rest_framework import serializers

from ..models import Title, Category

__all__ = ['TitleSerializer', 'CategorySerializer']


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'title', 'updated_at', 'is_bold', 'can_write', 'category')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'display_order')
