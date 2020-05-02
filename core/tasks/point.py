from django.db import transaction

import dramatiq
from ..models import Entry

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