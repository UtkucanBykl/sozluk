from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import Entry, Like, Dislike
from ..serializers import TitleSerializer, UserSerializer
from ..tasks import create_notification_info

__all__ = ['EntrySerializer']

User = get_user_model()


class ReadOnlyLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        fields = ('user',)
        read_only_fields = fields
        model = Like


class ReadOnlyDislikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        fields = ('user',)
        read_only_fields = fields
        model = Dislike


class EntrySerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    title_data = TitleSerializer(read_only=True, source='title')
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(),
        default=serializers.CurrentUserDefault()
    )
    is_like = serializers.BooleanField(read_only=True, default=False)
    is_dislike = serializers.BooleanField(read_only=True, default=False)
    like_count = serializers.IntegerField(default=0, read_only=True)
    dislike_count = serializers.IntegerField(default=0, read_only=True)
    likes = ReadOnlyLikeSerializer(many=True, read_only=True)
    dislikes = ReadOnlyDislikeSerializer(many=True, read_only=True)

    class Meta:
        model = Entry
        fields = (
            'user', 'updated_at', 'title_data', 'title', 'content', 'is_important', 'user', 'user_data', 'is_like', 'id',
            'like_count', 'dislike_count', 'likes', 'dislikes', 'is_dislike', 'status')

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if data.get("status") == "publish" and self.context.get("request").user.account_type == "rookie":
            data["status"] = "publish_by_rookie"
        return data

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
        if attrs.get('title') and not attrs.get('title').can_write:
            raise ValidationError('This title has not permission for write by users')
        return super().validate(attrs)
