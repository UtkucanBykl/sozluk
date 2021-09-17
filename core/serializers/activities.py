from rest_framework import serializers

from ..models import UserEmotionActivities
from ..serializers import EntrySerializer, UserEmotionSerializer

__all__ = ['UserEmotionLastActivities', 'UserEmotionLastActivitiesGet']


class UserEmotionLastActivities(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_detail = UserEmotionSerializer(source='user', many=False, read_only=True)
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)

    class Meta:
        model = UserEmotionActivities
        fields = ('user', 'user_detail', 'entry_detail', 'created_at')


class UserEmotionLastActivitiesGet(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user_detail = UserEmotionSerializer(source='user', many=False, read_only=True)

    class Meta:
        model = UserEmotionActivities
        fields = ('entry_detail', 'created_at', 'user_detail', 'activity_type')
