from django.contrib import  admin

from .actions import clone

__all__ = ['BaseAdmin']


class BaseAdmin(admin.ModelAdmin):
    actions = [clone]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(qs, 'actives'):
            return qs.actives()
        return qs

    def has_change_permission(self, request, obj=None):
        return False


