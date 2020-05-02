from django.utils import timezone
from django.db import transaction

from rest_framework import serializers

from ..models import Like, Dislike
from ..serializers import EntrySerializer

from ..tasks import create_notification_like, update_user_points, create_notification_dislike


__all__ = ['LikeSerializer', 'DislikeSerializer']


class LikeSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('entry', 'created_at', 'entry_detail', 'user')

    def save(self, **kwargs):
        save_return = super().save(**kwargs)
        entry = self.validated_data.get('entry')
        user = self.context['request'].user
        if hasattr(entry, 'id') and hasattr(user, 'id'):
            entry_id = entry.id
            user_id = user.id
            create_notification_like.send(user_id, entry_id)
            update_user_points.send(entry_id, -5)
            with transaction.atomic():
                entry.last_vote_time = timezone.now()
                entry.save()
        return save_return


class DislikeSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Dislike
        fields = ('entry', 'created_at', 'entry_detail', 'user')

    def save(self, **kwargs):
        save_return = super().save(**kwargs)
        entry = self.validated_data.get('entry')
        user = self.context['request'].user
        if hasattr(entry, 'id') and hasattr(user, 'id'):
            entry_id = entry.id
            user_id = user.id
            create_notification_dislike.send(user_id, entry_id)
            update_user_points.send(entry_id, -5)
            with transaction.atomic():
                entry.last_vote_time = timezone.now()
                entry.save()
        return save_return

