from django.contrib import  admin

__all__ = ['BaseAdmin']


class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(qs, 'actives'):
            return qs.actives()
        return qs
