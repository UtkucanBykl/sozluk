import dramatiq
from django.contrib.auth import get_user_model

from ..models import Notification, Entry


__all__ = ['create_notification_like']


User = get_user_model()


@dramatiq.actor
def create_notification_like(from_user_id, entry_id):
    try:
        print('dd')
        from_user = User.objects.get(id=from_user_id)
        entry = Entry.objects.get(id=entry_id)
        to_user = entry.user
        message = f'{from_user.username} adlı kullanıcı {entry.id} numaralı entrynizi beğendi.'
        Notification.objects.create(
            to_user=to_user,
            from_user=from_user,
            entry=entry,
            message=message,
            notification_type='like'
        )

    except BaseException as e:
        print(str(e))
