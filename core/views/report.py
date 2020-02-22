from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView


from ..serializers import ReportSerializer
from ..mixins import OwnerOrReadOnlyMixin

__all__ = ['ReportListCreateAPIView']


class ReportListCreateAPIView(OwnerOrReadOnlyMixin, ListCreateAPIView):
    serializer_class = ReportSerializer
    authentication_classes = (TokenAuthentication,)
    field = 'to_user'

    def get_queryset(self):
        return self.request.user.send_report.all()
