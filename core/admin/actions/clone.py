import random

__all__ = ["clone", "clone_title", "clone_user"]


def clone_title(modeladmin, request, queryset):
    for row in queryset:
        row.id = None
        row.title = f"{row.title} - {random.randint(0, 100000)}"
        row.slug = None
        row.old_id = None
        row.save()

clone_title.short_description = "Clone"


def clone(modeladmin, request, queryset):
    for row in queryset:
        row.id = None
        if hasattr(row, "old_id"):
            row.old_id = None
        if hasattr(row, "slug"):
            row.slug = None
        row.save()


def clone_user(modeladmin, request, queryset):
    for row in queryset:
        row.id = None
        row.old_id = None
        row.username = f"{row.username} - {random.randint(0, 100000)}"
        row.email = f"{random.randint(0, 10000)}{row.email}"

        row.save()