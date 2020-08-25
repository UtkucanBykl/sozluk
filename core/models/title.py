import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import Count, Q, Case, When, F, Value, BooleanField

from ..models import BaseModel, BaseManager, BaseModelQuery

__all__ = ['Title', 'Entry', 'Category']


User = get_user_model()


class TitleQuerySet(BaseModelQuery):
    def active_today(self):
        t = timezone.localtime(timezone.now())
        return self.filter(entry__updated_at__day=t.day, entry__updated_at__year=t.year,
                           entry__updated_at__month=t.month,
                           entry__status='publish').distinct()

    def order_points(self):
        return self.today_entry_counts().order_by('-is_bold', '-today_entry_counts')

    def have_user_entries(self, user):
        return self.filter(
            entry__user=user, entry__status='publish'
        )
    
    def today_entry_counts(self):
        t = timezone.localtime(timezone.now())
        return self.annotate(today_entry_count=Count('entry',
                                    filter=Q(entry__status='publish',
                                             entry__updated_at__day=t.day,
                                             entry__updated_at__year=t.year,
                                             entry__updated_at__month=t.month,
                                             ),
                                             distinct=True
                                    ))

    def total_entry_counts(self):
        return self.annotate(total_entry_count=Count('entry', filter=Q(entry__status='publish'), distinct=True))

    def full_text_search(self, value):
        return self.annotate(full_text=SearchVector('title')).filter(full_text=value)


class TitleManager(BaseManager):
    def get_queryset(self):
        return TitleQuerySet(self.model, using=self._db).select_related('category')

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

    def total_entry_counts(self):
        return self.get_queryset().total_entry_counts()


class EntryQuerySet(BaseModelQuery):
    def is_user_like(self, user):
        if user.is_authenticated:
            return self.annotate(is_like=Case(
                When(like_users__username=user.username, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
                )
            )
        return self.annotate(is_like=Value(False, output_field=BooleanField()))

    def is_user_dislike(self, user):
        if user.is_authenticated:
            return self.annotate(is_dislike=Case(
                When(dislike_users__username=user.username, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
                )
            )
        return self.annotate(is_like=Value(False, output_field=BooleanField()))

    def count_like_and_dislike(self, order_by=False):
        qs = self.annotate(like_count=Count('like')).annotate(dislike_count=Count('dislike'))
        if order_by == 'like':
            qs = qs.order_by('-like_count')
        elif order_by == 'dislike':
            qs = qs.order_by('-dislike')
        return qs


class EntryManager(BaseManager):
    def get_queryset(self):
        return EntryQuerySet(self.model, using=self._db)

    def is_user_like(self, user):
        return self.get_queryset().is_user_like(user)

    def count_like_and_dislike(self, order_by=False):
        return self.get_queryset().count_like_and_dislike(order_by)

    def is_user_dislike(self, user):
        return self.get_queryset().is_user_dislike(user)


class Title(BaseModel):
    title = models.CharField(max_length=40, unique=True)
    display_order = models.IntegerField(default=0)
    is_bold = models.BooleanField(default=False)
    can_write = models.BooleanField(default=True)
    category = models.ForeignKey('core.Category', null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name='titles', related_query_name='title')
    user = models.ForeignKey(User, null=True, blank=True, related_name='titles', on_delete=models.SET_NULL,
                             related_query_name='title')

    objects = TitleManager()

    def __str__(self):
        return self.title


class Entry(BaseModel):
    stages = (
        ('draft', 'draft'),
        ('publish', 'publish'),
        ('deleted', 'deleted'),
        ('morning', 'morning')
    )
    status = models.CharField(choices=stages, default='publish', max_length=25)
    title = models.ForeignKey('core.Title', related_name='entries', on_delete=models.CASCADE,
                              related_query_name='entry')
    user = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=500)
    is_important = models.BooleanField(default=False)
    last_vote_time = models.DateTimeField(default=timezone.now)

    objects = EntryManager()

    def __str__(self):
        return self.content


class Category(BaseModel):
    name = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-display_order']
