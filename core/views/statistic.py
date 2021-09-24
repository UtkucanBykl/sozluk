from rest_framework.views import APIView

from django.db.models import Q
from rest_framework.response import Response

from ..models import Entry, Title, User, Like, Dislike

from django.utils import timezone

__all__ = ['SozlukStatistics']


class SozlukStatistics(APIView):

    def get(self, request):
        t = timezone.localtime(timezone.now())
        today_entry_count = Entry.objects.filter(created_at__day=t.day, created_at__month=t.month, created_at__year=t.year).count()
        yesterday_entry_count = Entry.objects.filter(created_at__day=t.day - 1, created_at__month=t.month, created_at__year=t.year).count()
        this_month_entry_count = Entry.objects.filter(created_at__month=t.month).count()
        total_entry_count = Entry.objects.all().count()
        total_is_not_ukde_title_count = Title.objects.filter(is_ukde=False).count()
        total_user_count = User.objects.all().count()
        total_like_count = Like.objects.all().count()
        total_dislike_count = Dislike.objects.all().count()
        total_active_user = User.objects.filter(status='publish').count()
        total_active_rookie_user = User.objects.filter(account_type="rookie", status='publish').count()
        total_deleted_user = User.objects.filter(status='deleted').count()
        avg_user_entry = total_entry_count / total_active_user
        total_active_title = Title.objects.all().count()
        number_of_definitions_per_title = total_entry_count / total_active_title
        number_of_descriptions_per_author = total_entry_count / total_active_user
        avg_entry_day = this_month_entry_count / 30
        superusers_and_mods = [user.username for user in User.objects.filter(Q(account_type="mod") | Q(is_superuser=True))]

        return Response(
            {
                "today_entry_count": today_entry_count,
                "yesterday_entry_count": yesterday_entry_count,
                "this_month_entry_count": this_month_entry_count,
                "total_entry_count": total_entry_count,
                "total_is_not_ukde_title_count": total_is_not_ukde_title_count,
                "number_of_definitions_per_title": number_of_definitions_per_title,
                "avg_entry_day": avg_entry_day,
                "total_like_count": total_like_count,
                "total_dislike_count": total_dislike_count,
                "total_user_count": total_user_count,
                "total_active_user": total_active_user,
                "total_active_rookie_user": total_active_rookie_user,
                "total_deleted_user": total_deleted_user,
                "avg_user_entry": avg_user_entry,
                "number_of_descriptions_per_author": number_of_descriptions_per_author,
                "superusers_and_mods": superusers_and_mods
            }
        )


