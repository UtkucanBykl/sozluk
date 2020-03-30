from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Entry
from ..serializers import TitleSerializer
from ..tasks import create_notification_info

__all__ = ['EntrySerializer']

User = get_user_model()


class EntrySerializer(serializers.ModelSerializer):
    # user_data = UserSerializer(source='user', read_only=True)
    title_data = TitleSerializer(read_only=True, source='title')
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Entry
        fields = ('user', 'updated_at', 'title_data', 'title', 'content', 'is_important', 'user')

    def save(self, **kwargs):
        save_return = super().save(**kwargs)
        create_notification_info.send(self.validated_data.get('title').id, self.validated_data.get('user').id)
        return save_return
