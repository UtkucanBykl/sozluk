from django_filters import rest_framework

from ..models import Title


__all__ = ['TitleFilter']


class TitleFilter(rest_framework.FilterSet):
    category = rest_framework.CharFilter(field_name='category__name', lookup_expr='iexact')
    title = rest_framework.CharFilter(field_name='title', lookup_expr='iexact')
    entry_username = rest_framework.CharFilter(method='filter_by_username')
    today = rest_framework.BooleanFilter(method='get_today')
    full_text = rest_framework.CharFilter(method='get_full_text')
    followed = rest_framework.BooleanFilter(method="get_followed_title")

    class Meta:
        model = Title
        fields = ('category', 'title', 'today', 'full_text', "followed", 'is_ukde')

    def filter_by_username(self, queryset, name, value):
        return queryset.filter(entry__user__username=value, entry__status='publish').distinct()

    def get_today(self, queryset, name, value):
        return queryset.active_today()

    def get_full_text(self, queryset, name, value):
        return queryset.full_text_search(value)

    def get_followed_title(self, queryset, name, value):
        if self.request.user.is_authenticated:
            queryset = queryset.prefetch_related("follows")
            return queryset.filter(follows__user=self.request.user)
        return queryset

    def get_title_with_is_ukde(self, queryset):
        if self.request.user.is_authenticated:
            return queryset.get_titles_with_is_ukde()
        return queryset
