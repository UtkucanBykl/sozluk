from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Notification, Entry
from ..serializers import UserSerializer, EntrySerializer


__all__ = ['NotificationSerializer']

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    to_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    from_user_detail = UserSerializer(source='from_user', many=False, read_only=True, required=False)
    entry = serializers.PrimaryKeyRelatedField(queryset=Entry.objects.filter(), allow_null=True, allow_empty=True)
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(), allow_null=True, allow_empty=True)

    class Meta:
        model = Notification
        fields = (
            'entry', 'created_at', 'entry_detail', 'to_user', 'from_user_detail', 'message', 'notification_type', 'from_user'
        )
