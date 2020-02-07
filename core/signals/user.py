from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

__all__ = ['create_token']


@receiver(post_save, sender=get_user_model())
def create_token(sender, instance, *args, **kwargs):
    if kwargs['created']:
        Token.objects.create(user=instance)

