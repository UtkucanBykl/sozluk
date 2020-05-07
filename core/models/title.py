import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import Count, Q

from ..models import BaseModel, BaseManager, BaseModelQuery

__all__ = ['Title', 'Entry', 'Category']


User = get_user_model()


class TitleQuerySet(BaseModelQuery):
    def active_today(self):
        t = timezone.localtime(timezone.now())
        return self.filter(entries__updated_at__day=t.day, entries__updated_at__year=t.year,
                           entries__updated_at__month=t.month,
                           entries__status='publish').distinct()

    def order_points(self):
        return self.today_entry_counts().order_by('-is_bold', '-today_entry_counts')

    def have_user_entries(self, user):
        return self.filter(
            entries__user=user, entries__status='publish'
        )
    
    def today_entry_counts(self):
        t = timezone.localtime(timezone.now())
        return self.annotate(publish_entry_count=Count('entries',
                                    filter=Q(entries__status='publish',
                                             entries__updated_at__day=t.day,
                                             entries__updated_at__year=t.year,
                                             entries__updated_at__month=t.month,
                                             ),
                                             distinct=True
                                    ))

    def full_text_search(self, value):
        return self.annotate(full_text=SearchVector('title')).filter(full_text=value)


class TitleManager(BaseManager):
    def get_queryset(self):
        return TitleQuerySet(self.model, using=self._db)

    def active_today(self):
        return self.get_queryset().active_today()

    def today_entry_counts(self):
        return self.get_queryset().today_entry_counts()

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
    user = models.ForeignKey(User, null=True, blank=True, related_name='titles', on_delete=models.SET_NULL)

    objects = TitleManager()

    def __str__(self):
        return self.title


class Entry(BaseModel):
    title = models.ForeignKey('core.Title', related_name='entries', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=500)
    is_important = models.BooleanField(default=False)
    last_vote_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
