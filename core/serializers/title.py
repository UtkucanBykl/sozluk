from rest_framework import serializers

from ..models import Title, NotShowTitle, User, Entry
from ..serializers import UserSerializer

__all__ = ['TitleSerializer', 'NotShowTitleSerializer']


class TitleSerializer(serializers.ModelSerializer):
    total_entry_count = serializers.IntegerField(read_only=True, default=0)
    today_entry_count = serializers.IntegerField(read_only=True, default=0)
    user_detail = UserSerializer(source='user', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(),
        default=serializers.CurrentUserDefault()
    )
    first_entry_of_title = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'title', 'updated_at', 'is_bold', 'can_write', 'total_entry_count', 'today_entry_count',
            'created_at', 'user', 'is_ukde', 'first_entry_of_title', 'user_detail', 'status')

    def get_first_entry_of_title(self, title):
        entry = Entry.objects.filter(title=title.id).first()
        if entry and entry.user:
            return {"username": entry.user.username, "created_at": entry.created_at}
        return


class NotShowTitleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = NotShowTitle
        fields = ('user', 'title')
