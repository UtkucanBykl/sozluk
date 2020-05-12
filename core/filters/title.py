from django_filters import rest_framework

from ..models import Title


__all__ = ['TitleFilter']


class TitleFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__name', lookup_expr='iexact')
    title = rest_framework.CharFilter(field_name='title', lookup_expr='iexact')
    entry_username = rest_framework.CharFilter(method='filter_by_username')

    class Meta:
        model = Title
        fields = ('category', 'title')

    def filter_by_username(self, queryset, name, value):
        return queryset.filter(entry__user__username=value, entry__status='publish').distinct()