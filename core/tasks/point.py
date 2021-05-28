from django.db import transaction

import dramatiq
from ..models import Entry, User

__all__ = ['update_user_points', 'update_user_points_follow_or_title_create']


@dramatiq.actor
def update_user_points(entry_id, point):
    try:
        entry = Entry.objects.get(id=entry_id)
    except:
        return
    with transaction.atomic():
        user = entry.user
        user.point += point
        user.save()
    return user.point


@dramatiq.actor
def update_user_points_follow_or_title_create(user_id, point):
    try:
        user = User.objects.get(id=user_id)
    except:
        return
    with transaction.atomic():
        user.point += point
        user.save()
    return user.point