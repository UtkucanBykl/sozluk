from django_filters import rest_framework

from ..models import Title


__all__ = ['TitleFilter']


class TitleFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__name', lookup_expr='iexact')
    title = rest_framework.CharFilter(field_name='title', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ('category', 'title')
