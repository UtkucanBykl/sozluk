from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Report, Entry
from ..serializers import UserSerializer, EntrySerializer


__all__ = ['ReportSerializer']

User = get_user_model()


class ReportSerializer(serializers.ModelSerializer):
    entry_detail = EntrySerializer(source='entry', many=False, read_only=True)
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_user_detail = UserSerializer(source='to_user', many=False, read_only=True, required=False)
    entry = serializers.PrimaryKeyRelatedField(queryset=Entry.objects.filter(), allow_null=True, allow_empty=True)
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(), allow_null=True, allow_empty=True)

    class Meta:
        model = Report
        fields = (
            'entry', 'created_at', 'entry_detail', 'to_user', 'to_user_detail', 'content', 'report_type', 'from_user'
        )
