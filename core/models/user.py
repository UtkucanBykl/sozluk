from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from ..models import BaseModel, BaseModelWithDelete


__all__ = ['User', 'Like', 'Dislike']


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

    username = models.CharField(
        max_length=140, unique=True
    )
    email = models.EmailField(
        verbose_name=_('email address')
    )
    first_name = models.CharField(
        max_length=255, verbose_name=_('first name'), null=True, blank=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name=_('last name'), null=True, blank=True
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_('active')
    )
    is_staff = models.BooleanField(
        default=False, verbose_name=_('staff status')
    )
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_('date joined')
    )

    likes = models.ManyToManyField('core.Entry', related_name='like_users', through='core.Like', blank=True)
    title_follows = models.ManyToManyField('core.Title', related_name='followers', through='core.TitleFollow', blank=True)
    user_follows = models.ManyToManyField('self', symmetrical=False, through='core.UserFollow', blank=True)
    dislikes = models.ManyToManyField('core.Entry', related_name='dislike_users', through='core.Dislike', blank=True)
    point = models.IntegerField(default=0)

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        constraints = [
            models.UniqueConstraint(fields=['username'], name='username_unique'),
            models.UniqueConstraint(fields=['email'], name='email_unique')
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
