from rest_framework import serializers

from ..models import PunishUser

__all__ = ['PunishSerializer']


class PunishSerializer(serializers.ModelSerializer):

    class Meta:
        model = PunishUser
        fields = ('punished_user', 'punish_description', 'punish_finish_date', 'status', 'created_at')
