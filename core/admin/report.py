from django.contrib import admin

from .base import BaseAdmin
from ..models import Report

__all__ = ['ReportAdmin']


@admin.register(Report)
class ReportAdmin(BaseAdmin):
    list_display = ('status', 'from_user', 'to_user', 'entry', 'report_type')
    list_select_related = ('from_user', 'to_user', 'entry')
    search_fields = (
        'from_user__username', 'from_user__email', 'to_user__username', 'to_user__email'
    )
    list_filter = ('report_type',)
