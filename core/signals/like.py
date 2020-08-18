from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Like, Dislike


@receiver(post_save, sender=Like)
def delete_dislike_if_it_is_there(sender, instance, *args, **kwargs):
    Dislike.objects.filter(user=instance.user, entry=instance.entry).delete()


@receiver(post_save, sender=Dislike)
def delete_dislike_if_it_is_there(sender, instance, *args, **kwargs):
    Like.objects.filter(user=instance.user, entry=instance.entry).delete()
