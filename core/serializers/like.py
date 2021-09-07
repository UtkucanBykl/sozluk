from rest_framework import serializers

from ..models import Like, Dislike, Favorite
from ..serializers import EntrySerializer, UserEmotionSerializer

__all__ = ['LikeSerializer', 'DislikeSerializer', 'FavoriteSerializer', 'EntryLikeSerializer', 'EntryDislikeSerializer',
           'EntryFavoriteSerializer']


class LikeSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('entry', 'created_at', 'entry_detail', 'user')


class DislikeSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Dislike
        fields = ('entry', 'created_at', 'entry_detail', 'user')


class FavoriteSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = ('entry', 'created_at', 'entry_detail', 'user')


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
