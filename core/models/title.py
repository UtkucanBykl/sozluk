import datetime
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import (
    Count,
    Q,
    Case,
    When,
    F,
    Value,
    BooleanField,
    Exists,
    OuterRef,
)
from django.utils.text import slugify

from ..models import BaseModel, BaseManager, BaseModelQuery, Block


__all__ = ["Title", "Entry", "NotShowTitle"]


User = get_user_model()


class TitleQuerySet(BaseModelQuery):
    def active_today(self):
        t = timezone.localtime(timezone.now())
        return self.filter(
            entry__updated_at__day=t.day,
            entry__updated_at__year=t.year,
            entry__updated_at__month=t.month,
            entry__status="publish",
        ).distinct()

    def order_points(self):
        return self.today_entry_counts().order_by("-is_bold", "-today_entry_counts")

    def have_user_entries(self, user):
        return self.filter(entry__user=user, entry__status="publish")

    def today_entry_counts(self):
        t = timezone.localtime(timezone.now())
        return self.annotate(
            today_entry_count=Count(
                "entry",
                filter=Q(
                    entry__status="publish",
                    entry__updated_at__day=t.day,
                    entry__updated_at__year=t.year,
                    entry__updated_at__month=t.month,
                ),
                distinct=True,
            )
        ).prefetch_related("entries")

    def total_entry_counts(self):
        return self.annotate(
            total_entry_count=Count(
                "entry", filter=Q(entry__status="publish"), distinct=True
            )
        ).prefetch_related("entries")

    def full_text_search(self, value):
        return self.annotate(full_text=SearchVector("title")).filter(full_text=value)

    def get_titles_without_not_showing(self, user):
        if user.is_authenticated:
            not_show_title = NotShowTitle.objects.filter(
                title=OuterRef("pk"), user=user
            )
            return self.annotate(is_not_show=Exists(not_show_title)).filter(
                is_not_show=False
            )
        return self.filter()

    def get_titles_with_is_ukde(self):
        return self.filter(is_ukde=True)


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

    def total_entry_counts(self):
        return self.get_queryset().total_entry_counts()

    def get_titles_without_not_showing(self, user):
        return self.get_queryset().get_titles_without_not_showing(user)

    def get_titles_with_is_ukde(self, user):
        return self.get_queryset().get_titles_with_is_ukde(user)


class EntryQuerySet(BaseModelQuery):
    def is_user_like(self, user):
        if user.is_authenticated:
            return self.annotate(
                is_like=Case(
                    When(like_users__username=user.username, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        return self.annotate(is_like=Value(False, output_field=BooleanField()))

    def is_user_dislike(self, user):
        if user.is_authenticated:
            return self.annotate(
                is_dislike=Case(
                    When(dislike_users__username=user.username, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        return self.annotate(is_like=Value(False, output_field=BooleanField()))

    def is_user_favorite(self, user):
        if user.is_authenticated:
            return self.annotate(
                is_favorite=Case(
                    When(favorite_users__username=user.username, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        return self.annotate(is_favorite=Value(False, output_field=BooleanField()))

    def count_like_and_dislike_and_favorite(self, order_by=False):
        qs = self.annotate(
                like_count=Count("like")
            ).annotate(
            dislike_count=Count("dislike")
            ).annotate(
            favorite_count=Count("favorite")
            )
        if order_by == "like":
            qs = qs.order_by("-like_count")
        elif order_by == "dislike":
            qs = qs.order_by("-dislike")
        elif order_by == "favorite":
            qs = qs.order_by("-favorite")
        return qs

    def get_without_block_user(self, user):
        if user.is_authenticated:
            block_user = Block.objects.filter(
                blocked_user=OuterRef("user__pk"), user=user, is_entry=True
            )
            blocked_user = Block.objects.filter(
                blocked_user=user, user=OuterRef("user__pk"), is_entry=True
            )
            return (
                self.annotate(is_block_user=Exists(block_user))
                .annotate(is_blocked_user=Exists(blocked_user))
                .exclude(Q(is_block_user=True) | Q(is_blocked_user=True))
            )
        return self.filter()


class EntryManager(BaseManager):
    def get_queryset(self):
        return EntryQuerySet(self.model, using=self._db)

    def is_user_like(self, user):
        return self.get_queryset().is_user_like(user)

    def count_like_and_dislike_and_favorite(self, order_by=False):
        return self.get_queryset().count_like_and_dislike_and_favorite(order_by)

    def is_user_dislike(self, user):
        return self.get_queryset().is_user_dislike(user)

    def is_user_favorite(self, user):
        return self.get_queryset().is_user_favorite(user)

    def get_without_block_user(self, user):
        return self.get_queryset().get_without_block_user(user)


class Title(BaseModel):
    title = models.CharField(max_length=400, unique=True)
    slug = models.SlugField(max_length=140)
    old_id = models.PositiveIntegerField(null=True, blank=True)
    display_order = models.IntegerField(default=0)
    is_bold = models.BooleanField(default=False)
    can_write = models.BooleanField(default=True)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="titles",
        on_delete=models.SET_NULL,
        related_query_name="title",
    )
    redirect = models.ForeignKey(
        "core.Title",
        null=True,
        blank=True,
        related_name="redirects",
        on_delete=models.SET_NULL
    )
    is_ukde = models.BooleanField(default=True)

    objects = TitleManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="slug_unique"),
            models.UniqueConstraint(fields=["old_id"], name="title_old_id_unique", condition=Q(old_id__isnull=False))
        ]
        indexes = [
            models.Index(fields=["status"], name="status_index")
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save()


class Entry(BaseModel):
    stages = (
        ("draft", "draft"),
        ("publish", "publish"),
        ("publish_by_rookie", "publish by rookie"),
        ("deleted", "deleted"),
        ("morning", "morning"),
        ("deleted_by_admin", "deleted by admin"),
    )
    old_id = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(choices=stages, default="publish", max_length=25)
    title = models.ForeignKey(
        "core.Title",
        related_name="entries",
        on_delete=models.CASCADE,
        related_query_name="entry",
    )
    user = models.ForeignKey(
        User, related_name="entries", on_delete=models.CASCADE, blank=True, null=True
    )
    content = models.TextField(max_length=500)
    is_important = models.BooleanField(default=False)
    is_tematik = models.BooleanField(default=False)
    last_vote_time = models.DateTimeField(default=timezone.now)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    count_favorite = models.IntegerField(default=0)

    objects = EntryManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["old_id"], name="entry_old_id_unique", condition=Q(old_id__isnull=False))
        ]
        indexes = [
            models.Index(fields=("title", "updated_at", "status"), name="today_index"),
            models.Index(fields=("title", "status"), name="total_index")
        ]

    def __str__(self):
        return self.content

    def delete(self, user=None, hard=False):
        if hard:
            return super().delete()

        if user.is_superuser and self.user != user:

            self.status = "deleted_by_admin"
            self.deleted_at = timezone.now()
            return self.save()
        else:
            self.status = "deleted"
            self.deleted_at = timezone.now()
            return self.save()


class NotShowTitle(BaseModel):
    title = models.ForeignKey(
        "core.Title", related_name="not_show_titles", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name="not_show_titles",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "user"], name="now_show_title_unique"
            )
        ]

    def __str__(self):
        return self.title.title + " " + self.user.username
