from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Entry
from ..serializers import TitleSerializer, UserSerializer
from ..tasks import create_notification_info

__all__ = ['EntrySerializer']

User = get_user_model()


class EntrySerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    title_data = TitleSerializer(read_only=True, source='title')
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(),
        default=serializers.CurrentUserDefault()
    )
    is_like = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(default=0, read_only=True)
    dislike_count = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Entry
        fields = (
            'user', 'updated_at', 'title_data', 'title', 'content', 'is_important', 'user', 'user_data', 'is_like', 'id',
            'like_count', 'dislike_count')

    def to_internal_value(self, data):
        new_data = data.copy()
        title_id = self.context['view'].kwargs.get('title_id')
        new_data['title'] = title_id
        return super().to_internal_value(new_data)

    def to_representation(self, instance):
        return super().to_representation(instance)

    def save(self, **kwargs):
        save_return = super().save(**kwargs)
        title = self.validated_data.get('title')
        user = self.validated_data.get('user')
        if hasattr(title, 'id') and hasattr(user, 'id'):
            title_id = title.id
            user_id = user.id
            create_notification_info.send(title_id, user_id)
        return save_return

    def validate(self, attrs):
        if not attrs.get('title').can_write:
            raise ValidationError('This title has not permission for write by users')
        return super().validate(attrs)

    def get_is_like(self, obj):
        return obj.is_like if hasattr(obj, 'is_like') else None
