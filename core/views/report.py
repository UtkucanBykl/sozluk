from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import ReportSerializer
from ..mixins import OwnerOrReadOnlyMixin
from ..models import Report

__all__ = ['ReportListCreateAPIView']


class ReportListCreateAPIView(OwnerOrReadOnlyMixin, ListCreateAPIView):
    serializer_class = ReportSerializer
    authentication_classes = (TokenAuthentication,)
    field = 'to_user'
    http_method_names = ["post", "get"]

    def get_queryset(self):
        return self.request.user.send_report.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        entry_id = self.request.data.get('entry', {})
        reported_entry = Report.objects.filter(from_user=self.request.user, entry=entry_id)
        if reported_entry:
            return Response({"error_message": "Bu entry sizin tarafınızdan zaten şikayet edildi."})
        else:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)