from rest_framework.pagination import PageNumberPagination

__all__ = ['StandartPagination', 'LargePagination']


class StandartPagination(PageNumberPagination):
    page_size = 10


class LargePagination(PageNumberPagination):
    page_size = 100
