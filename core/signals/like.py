from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Like, Dislike


@receiver(post_save, sender=Like)
def delete_dislike_if_it_is_there(sender, instance, *args, **kwargs):
    dislike_obj = Dislike.objects.filter(user=instance.user, entry=instance.entry)
    if dislike_obj.exists():
        dislike_obj.delete()


@receiver(post_save, sender=Dislike)
def delete_dislike_if_it_is_there(sender, instance, *args, **kwargs):
    like_obj = Like.objects.filter(user=instance.user, entry=instance.entry)
    if like_obj.exists():
        like_obj.delete()
