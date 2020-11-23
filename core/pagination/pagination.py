from rest_framework.pagination import PageNumberPagination

__all__ = ['StandardPagination', 'LargePagination', "StandardTitlePagination", "StandardEntryPagination"]


class StandardPagination(PageNumberPagination):
    page_size = 10


class LargePagination(PageNumberPagination):
    page_size = 100


class StandardTitlePagination(PageNumberPagination):
    page_size = 33


class StandardEntryPagination(PageNumberPagination):
    page_size = 10
