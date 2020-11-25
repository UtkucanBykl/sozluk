from rest_framework import serializers

from ..models import Suggested
from ..serializers import TitleSerializer

__all__ = ["SuggestedListSerializer", "SuggestedCreateSerializer"]


class SuggestedListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "message", "suggested_type", "created_at", "updated_at")
        model = Suggested
        read_only_fields = fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["title"] = (
            TitleSerializer(instance.title, context=self.context, read_only=True).data if instance.title else None
        )
        return data


class SuggestedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "message", "suggested_type")
        model = Suggested
