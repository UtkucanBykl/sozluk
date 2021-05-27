from rest_framework import serializers
from django.utils import timezone


from ..serializers import UserMessageSerializer, UserSerializer

from ..models import Message

__all__ = ['MessageSerializer']


class MessageSerializer(serializers.ModelSerializer):
    sender_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sender_user_detail = UserMessageSerializer(source='sender_user', read_only=True, many=False)
    receiver_user_detail = UserMessageSerializer(source='receiver_user', read_only=True, many=False)

    class Meta:
        model = Message
        fields = ('id', 'sender_user', 'sender_user_detail', 'receiver_user', 'receiver_user_detail',
                  'content', 'created_at')

    def save(self, **kwargs):
        save_return = super().save(**kwargs)
        return save_return
