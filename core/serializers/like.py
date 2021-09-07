from django.utils import timezone
from django.db import transaction

from rest_framework import serializers
from rest_framework.response import Response

from ..models import Like, Dislike, Favorite, Entry, UserEmotionActivities
from ..serializers import EntrySerializer, UserSerializer, UserEmotionSerializer

from ..tasks import create_notification_like, update_user_points, create_notification_dislike, \
    create_notification_favorite, increment_like_dislike_favorite

__all__ = ['LikeSerializer', 'DislikeSerializer', 'FavoriteSerializer', 'EntryLikeSerializer', 'EntryDislikeSerializer',
           'EntryFavoriteSerializer']


class LikeSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('entry', 'created_at', 'entry_detail', 'user')

    def save(self, **kwargs):
        entry = self.validated_data.get('entry')
        user = self.context['request'].user
        like = Like.objects.filter(user=user.id, entry=entry.id)
        if like:
            return Response({"error_message": "Bu içeriği zaten beğendiniz."})
        else:
            save_return = super().save(**kwargs)
            if hasattr(entry, 'id') and hasattr(user, 'id'):
                UserEmotionActivities.objects.create(user=user, entry=entry)
                entry_id = entry.id
                user_id = user.id
                create_notification_like.send(user_id, entry_id)
                update_user_points.send(entry_id, 1)
                increment_like_dislike_favorite.send("like", entry_id)
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
        entry = self.validated_data.get('entry')
        user = self.context['request'].user
        dislike = Dislike.objects.filter(user=user.id, entry=entry.id)
        if dislike:
            return Response({"error_message": "Zaten bu içeriği beğenmediniz."})
        else:
            save_return = super().save(**kwargs)
            if hasattr(entry, 'id') and hasattr(user, 'id'):
                UserEmotionActivities.objects.create(user=user, entry=entry)
                entry_id = entry.id
                user_id = user.id
                create_notification_dislike.send(user_id, entry_id)
                update_user_points.send(entry_id, -1)
                increment_like_dislike_favorite.send("dislike", entry_id)
                with transaction.atomic():
                    entry.last_vote_time = timezone.now()
                    entry.save()
            return save_return


class FavoriteSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ('entry', 'created_at', 'entry_detail', 'user')

    def save(self, **kwargs):
        entry = self.validated_data.get('entry')
        user = self.context['request'].user
        favorite = Favorite.objects.filter(user=user.id, entry=entry.id)
        if favorite:
            return Response({"error_message": "Zaten bu içeriği favorilediniz."})
        else:
            save_return = super().save(**kwargs)
            if hasattr(entry, 'id') and hasattr(user, 'id'):
                UserEmotionActivities.objects.create(user=user, entry=entry)
                entry_id = entry.id
                user_id = user.id
                create_notification_favorite(user_id, entry_id)
                update_user_points.send(entry_id, 3)
                increment_like_dislike_favorite.send("favorite", entry_id)
                with transaction.atomic():
                    entry.last_vote_time = timezone.now()
                    entry.save()
            return save_return


class EntryLikeSerializer(serializers.ModelSerializer):
    user = UserEmotionSerializer()

    class Meta:
        model = Like
        fields = ('user', 'entry')


class EntryDislikeSerializer(serializers.ModelSerializer):
    user = UserEmotionSerializer()

    class Meta:
        model = Dislike
        fields = ('user', 'entry')


class EntryFavoriteSerializer(serializers.ModelSerializer):
    user = UserEmotionSerializer()

    class Meta:
        model = Favorite
        fields = ('user', 'entry')
