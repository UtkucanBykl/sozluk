from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Notification, Entry, Title
from ..serializers import UserSerializer, EntrySerializer


__all__ = ['NotificationSerializer']

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    sender_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    receiver_user_detail = UserSerializer(source='receiver_user', many=False, read_only=True, required=False)
    entry = serializers.PrimaryKeyRelatedField(queryset=Entry.objects.filter(), allow_null=True, allow_empty=True)
    receiver_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(), allow_null=True, allow_empty=True)
    title = serializers.PrimaryKeyRelatedField(queryset=Title.objects.filter(), allow_null=True, allow_empty=True)

    class Meta:
        model = Notification
        fields = (
            'entry', 'title', 'created_at', 'entry_detail', 'sender_user', 'receiver_user_detail', 'message',
            'notification_type', 'receiver_user'
        )
