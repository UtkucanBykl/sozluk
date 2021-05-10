from rest_framework import serializers

from ..models import Title, Category, NotShowTitle, User
from ..serializers import UserSerializer
from ..tasks.notification import create_notification_title_with_username

from rest_framework import status
from rest_framework.response import Response

__all__ = ['TitleSerializer', 'CategorySerializer', 'NotShowTitleSerializer']


class TitleSerializer(serializers.ModelSerializer):
    total_entry_count = serializers.IntegerField(read_only=True, default=0)
    today_entry_count = serializers.IntegerField(read_only=True, default=0)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Title
        fields = (
        'id', 'title', 'updated_at', 'is_bold', 'can_write', 'category', 'total_entry_count', 'today_entry_count',
        'created_at', 'user')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category, read_only=True, many=False).data
        return data

    def save(self, **kwargs):
        save_return = super().save(**kwargs)
        title = self.validated_data.get('title')
        user = self.context['request'].user
        is_username = User.objects.filter(username=title).first()
        if is_username and hasattr(is_username, 'id'):
            create_notification_title_with_username.send(user.id, title, is_username.id)
        return save_return


class CategorySerializer(serializers.ModelSerializer):
    title_count = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'display_order', 'title_count')


class NotShowTitleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = NotShowTitle
        fields = ('user', 'title')
