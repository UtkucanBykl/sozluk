from django_filters import rest_framework

from ..models import Entry


__all__ = ['EntryFilter']


class EntryFilter(rest_framework.FilterSet):
    user = rest_framework.CharFilter(field_name='user__username', lookup_expr='iexact')
    content = rest_framework.CharFilter(field_name='content', lookup_expr='iexact')

    class Meta:
        model = Entry
        fields = ('content', 'user')
