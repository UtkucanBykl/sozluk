from rest_framework import serializers

from ..models import Title, Category, NotShowTitle, User, Entry
from ..serializers import UserSerializer

__all__ = ['TitleSerializer', 'CategorySerializer', 'NotShowTitleSerializer']


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
            'id', 'title', 'updated_at', 'is_bold', 'can_write', 'category', 'total_entry_count', 'today_entry_count',
            'created_at', 'user', 'is_ukde', 'first_entry_of_title', 'user_detail', 'status')

    def get_first_entry_of_title(self, title):
        entry = Entry.objects.filter(title=title.id).first()
        if entry and entry.user:
            return {"username": entry.user.username, "created_at": entry.created_at}
        return

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category, read_only=True, many=False).data
        return data


class CategorySerializer(serializers.ModelSerializer):
    title_count = serializers.IntegerField(default=0, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'display_order', 'title_count')


class NotShowTitleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = NotShowTitle
        fields = ('user', 'title')
