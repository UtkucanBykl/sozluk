from rest_framework import serializers

from ..models import Title, Category

__all__ = ['TitleSerializer', 'CategorySerializer']


class TitleSerializer(serializers.ModelSerializer):
    total_entry_count = serializers.IntegerField(read_only=True, default=0)
    today_entry_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Title
        fields = ('id', 'title', 'updated_at', 'is_bold', 'can_write', 'category', 'total_entry_count', 'today_entry_count')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category, read_only=True, many=False).data
        return data


class CategorySerializer(serializers.ModelSerializer):
    title_count = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'display_order', 'title_count')
