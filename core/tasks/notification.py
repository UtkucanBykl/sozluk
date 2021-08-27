import dramatiq
from django.contrib.auth import get_user_model

from ..models import Notification, Entry, Title

__all__ = ['create_notification_like', 'create_notification_info', 'create_notification_dislike',
           'create_notification_favorite', 'create_notification_title_with_username',
           'create_notification_entry_create_info_to_title_user']

User = get_user_model()


@dramatiq.actor
def create_notification_like(from_user_id, entry_id):
    try:
        sender_user = User.objects.get(id=from_user_id)
        entry = Entry.objects.get(id=entry_id)
        receiver_user = entry.user
        message = f'<i class="fa fa-info-circle"></i><a href="/author/{sender_user.id}">{sender_user.username}</a> adlı kullanıcı {entry.id} numaralı entrynizi ' \
                  f'beğendi. '
        Notification.objects.create(
            sender_user=sender_user,
            receiver_user=receiver_user,
            entry=entry,
            message=message,
            notification_type='like'
        )

    except BaseException as e:
        print(str(e))


@dramatiq.actor
def create_notification_dislike(from_user_id, entry_id):
    try:
        sender_user = User.objects.get(id=from_user_id)
        entry = Entry.objects.get(id=entry_id)
        receiver_user = entry.user
        message = f'<i class="fa fa-info-circle"></i><a href="/author/{sender_user.id}">{sender_user.username}</a> {entry.id} numaralı entrynizi ' \
                  f'beğenmedi. '
        Notification.objects.create(
            sender_user=sender_user,
            receiver_user=receiver_user,
            entry=entry,
            message=message,
            notification_type='like'
        )

    except BaseException as e:
        print(str(e))


@dramatiq.actor
def create_notification_info(title_id, user_id):
    try:
        title = Title.objects.get(id=title_id)
        message = f'<i class="fa fa-info-circle"></i><a href="/{title.title}/{title.id}/{title.category}">{title.title}</a> başlığına yeni bir entry girildi.'
        for user in title.followers.exclude(id=user_id):
            Notification.objects.create(
                receiver_user=user,
                title=title,
                message=message,
                notification_type='info'
            )
    except BaseException as e:
        print(str(e))


@dramatiq.actor
def create_notification_favorite(from_user_id, entry_id):
    try:
        sender_user = User.objects.get(id=from_user_id)
        entry = Entry.objects.get(id=entry_id)
        receiver_user = entry.user
        message = f'<i class="fa fa-info-circle"></i><a href="/author/{sender_user.id}">{sender_user.username}</a> adlı kullanıcı {entry.id} numaralı ' \
                  f'entrynizi favoriledi. '
        Notification.objects.create(
            sender_user=sender_user,
            receiver_user=receiver_user,
            entry=entry,
            message=message,
            notification_type='favorite'
        )

    except BaseException as e:
        print(str(e))


@dramatiq.actor
def create_notification_title_with_username(from_user_id, title_name, receiver):
    try:
        sender_user = User.objects.get(id=from_user_id)
        title = Title.objects.filter(title=title_name)
        receiver_user = User.objects.get(username=receiver)
        message = f'<i class="fa fa-info-circle"></i>Kullanıcı adınıza ait nickaltı <a href="/{title.title}/{title.id}/{title.category}">' \
                  f'({title.title})</a> başlığı oluşturulmuştur. '
        Notification.objects.create(
            sender_user=sender_user,
            receiver_user=receiver_user,
            title=title,
            message=message,
            notification_type='title_with_username'
        )
    except BaseException as e:
        print(str(e))


@dramatiq.actor
def create_notification_entry_create_info_to_title_user(from_user_id, title_name, to_username):
    try:
        sender_user = User.objects.get(id=from_user_id)
        title = Title.objects.filter(title=title_name)
        to_user = User.objects.get(username=to_username)
        message = f'<i class="fa fa-info-circle"></i><a href="/author/{sender_user.id}">{sender_user.username}</a> ' \
                  f'isimli kullanıcı oluşturmuş olduğunuz <a href="/{title.title}/{title.id}/{title.category}">' \
                  f'{title.title}</a> başlığına entry yazdı. '
        Notification.objects.create(
            sender_user=sender_user,
            receiver_user=to_user,
            title=title,
            message=message,
            notification_type='info_title_entries'
        )
    except BaseException as e:
        print(str(e))
