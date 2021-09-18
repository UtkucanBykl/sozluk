import dramatiq
from django.contrib.auth import get_user_model

from ..models import Notification, Entry, Title

__all__ = ['combine_two_titles']

User = get_user_model()


@dramatiq.actor
def combine_two_titles(from_title_id, to_title_id, user_id):
    try:
        receiver_user = User.objects.get(id=user_id)
        from_title = Title.objects.get(id=from_title_id)
        to_title = Title.objects.get(id=to_title_id)
        if from_title and to_title:
            from_title_entries = Entry.objects.filter(title=from_title_id)
            for entry in from_title_entries:
                entry.title = to_title
                entry.save()

            from_title.status = "deleted"
            from_title.save()

            message = f'{from_title.title} başlığındaki girdiler {to_title.title} başlığına başarıyla taşınmıştır.'
            Notification.objects.create(
                sender_user=None,
                receiver_user=receiver_user,
                message=message,
                notification_type='info'
            )
        else:
            message = f'{from_title.title} başlığındaki girdiler {to_title.title} başlığına taşınırken bir hata oluştu. Lütfen tekrar deneyiniz.'
            Notification.objects.create(
                sender_user=None,
                receiver_user=receiver_user,
                message=message,
                notification_type='info'
            )
    except BaseException as e:
        print(str(e))
