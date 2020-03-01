import datetime

from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import Count, Q

from ..models import BaseModel, BaseManager, BaseModelQuery

__all__ = ['Title', 'Entry', 'Category']


User = get_user_model()


class TitleQuerySet(BaseModelQuery):
    def active_today(self):
        return self.filter(entries__updated_at__day=datetime.datetime.now().day,
                           entries__status='publish', is_deleted=False).distinct()

    def order_points(self):
        publish_entry_count = Count('entries',
                                    filter=Q(status='publish',
                                             updated_at__day=datetime.datetime.now().day,
                                             is_deleted=False
                                             )
                                    )
        return self.annotate(
            entry_count=publish_entry_count
        ).order_by('-is_bold', '-entry_count')

    def have_user_entries(self, user):
        return self.filter(
            entries__user=user, entries__is_deleted=False
        )

    def full_text_search(self, value):
        return self.annotate(full_text=SearchVector('title')).filter(full_text=value)


class TitleManager(BaseManager):
    def get_queryset(self):
        return TitleQuerySet(self.model, using=self._db)

    def active_today(self):
        return self.get_queryset().active_today()

    def order_by_entry_count(self):
        return self.get_queryset().order_points()

    def have_user_entries(self, user):
        return self.get_queryset().have_user_entries(user)

    def full_text_search(self, value):
        return self.get_queryset().full_text_search(value)


class Title(BaseModel):
    title = models.CharField(max_length=40, unique=True)
    display_order = models.IntegerField(default=0)
    is_bold = models.BooleanField(default=False)
    can_write = models.BooleanField(default=True)
    category = models.ForeignKey('core.Category', null=True, blank=True, on_delete=models.SET_NULL)

    objects = TitleManager()

    def __str__(self):
        return self.title


class Entry(BaseModel):
    title = models.ForeignKey('core.Title', related_name='entries', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=500)
    is_important = models.BooleanField(default=False)


    def __str__(self):
        return self.content


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
