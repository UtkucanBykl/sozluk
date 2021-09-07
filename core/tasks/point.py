from django.db import transaction

import dramatiq
from ..models import Entry, User

__all__ = ['update_user_points', 'update_user_points_follow_or_title_create',
           'increment_like_dislike_favorite', 'decrement_like_dislike_favorite']


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


@dramatiq.actor
def increment_like_dislike_favorite(emotion_type, entry_id):
    try:
        entry = Entry.objects.get(id=entry_id)
    except:
        return
    with transaction.atomic():
        if emotion_type == 'like':
            entry.count_like += 1
            entry.save()
            return entry.count_like
        elif emotion_type == 'dislike':
            entry.count_dislike += 1
            entry.save()
            return entry.count_dislike
        elif emotion_type == 'favorite':
            entry.count_favorite += 1
            entry.save()
            return entry.count_favorite


@dramatiq.actor
def decrement_like_dislike_favorite(emotion_type, entry_id):
    try:
        entry = Entry.objects.get(id=entry_id)
    except:
        return
    with transaction.atomic():
        if emotion_type == 'like':
            entry.count_like -= 1
            entry.save()
            return entry.count_like
        elif emotion_type == 'dislike':
            entry.count_dislike -= 1
            entry.save()
            return entry.count_dislike
        elif emotion_type == 'favorite':
            entry.count_favorite -= 1
            entry.save()
            return entry.count_favorite
