from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ..models import BaseModel, BaseModelWithDelete
from ..utils import generate_upload_path

__all__ = ['User', 'Like', 'Dislike', "Block", "Favorite"]


class UserManager(BaseUserManager):
    """
    Our custom User model's basic needs.
    """

    use_in_migrations = True

    def create_user(
        self,
        username,
        email,
        first_name=None,
        last_name=None,
        password=None,
    ):
        if not email:
            raise ValueError(
                _('Users must have an email address')
            )

        user_create_fields = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }

        user = self.model(**user_create_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username,
        email,
        first_name=None,
        last_name=None,
        password=None,
    ):
        user = self.create_user(
            username,
            email,
            first_name,
            last_name,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(
    BaseModel,
    AbstractBaseUser,
    PermissionsMixin,
):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    old_id = models.PositiveIntegerField(verbose_name="Old ID", blank=True, null=True)
    username = models.CharField(
        max_length=140, unique=True
    )
    email = models.EmailField(
        verbose_name=_('email address')
    )
    first_name = models.CharField(
        max_length=255, verbose_name=_('first name'), default="", blank=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name=_('last name'), default="", blank=True
    )
    bio = models.TextField(
        max_length=255, verbose_name=_('Bio'), default="", blank=True
    )
    show_bio = models.BooleanField(verbose_name=_("Show Bio?"), default=True)
    is_active = models.BooleanField(
        default=True, verbose_name=_('active')
    )
    is_staff = models.BooleanField(
        default=False, verbose_name=_('staff status')
    )
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_('date joined')
    )

    city = models.CharField(
        max_length=15, default="", blank=True, verbose_name=_('city where you live')
    )
    is_show_city = models.BooleanField(verbose_name=_('Everyone to see'), default=False)

    birth_day = models.DateField(
        verbose_name="Birth day", null=True, blank=True
    )
    is_show_birth_day = models.BooleanField(verbose_name=_('Everyone to see'), default=False)

    genders = (
        ("female", "Female"),
        ("male", "Male"),
        ("uncertain", "I don't want to specify.")
    )
    gender = models.CharField(choices=genders, default="uncertain", max_length=25)
    is_show_gender = models.BooleanField(verbose_name=_('Everyone to see'), default=False)

    twitter_username = models.CharField(max_length=255, default="")

    facebook_profile = models.CharField(max_length=500, default="")

    account_types = (
        ("rookie", "Rookie"),
        ("normal", "Normal"),
        ("mod", "Moderator")
    )
    account_type = models.CharField(choices=account_types, default="rookie", max_length=25)
    likes = models.ManyToManyField('core.Entry', related_name='like_users', through='core.Like', blank=True)
    title_follows = models.ManyToManyField('core.Title', related_name='followers', through='core.TitleFollow', blank=True)
    user_follows = models.ManyToManyField('self', symmetrical=False, through='core.UserFollow', blank=True)
    dislikes = models.ManyToManyField('core.Entry', related_name='dislike_users', through='core.Dislike', blank=True)
    point = models.IntegerField(default=0)
    profile_picture = models.ImageField(max_length=500, upload_to=generate_upload_path, null=True, blank=True)
    favorites = models.ManyToManyField('core.Entry', related_name='favorite_users', through='core.Favorite', blank=True)

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        constraints = [
            models.UniqueConstraint(fields=['username'], name='username_unique'),
            models.UniqueConstraint(fields=['email'], name='email_unique'),
            models.UniqueConstraint(fields=["old_id"], name="user_old_id_unique", condition=Q(old_id__isnull=False))
        ]

    def __str__(self):
        return self.username


class Like(BaseModelWithDelete):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    entry = models.ForeignKey('core.Entry', on_delete=models.CASCADE, blank=True, null=True,
                              related_query_name='like', related_name='likes')

    def __str__(self):
        return self.user.username + 'likes' + str(self.entry.id)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'entry'], name='like_unique')
        ]


class Dislike(BaseModelWithDelete):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    entry = models.ForeignKey('core.Entry', on_delete=models.CASCADE, blank=True, null=True,
                              related_query_name='dislike', related_name='dislikes')

    def __str__(self):
        return self.user.username + 'likes' + str(self.entry.id)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'entry'], name='dislike_unique')
        ]


class Block(BaseModelWithDelete):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="block_list")
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_message = models.BooleanField(default=True)
    is_entry = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username + " " + self.blocked_user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'blocked_user'], name='blockuser_unique')
        ]


class Favorite(BaseModelWithDelete):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    entry = models.ForeignKey('core.Entry', on_delete=models.CASCADE, blank=True, null=True,
                              related_query_name='favorite', related_name='favorites')

    def __str__(self):
        return self.user.username + 'favorites' + str(self.entry.id)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'entry'], name='favorite_unique')
        ]