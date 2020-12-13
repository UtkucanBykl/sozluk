from rest_framework.pagination import PageNumberPagination

__all__ = ['StandardPagination', 'LargePagination', "StandardTitlePagination", "StandardEntryPagination"]


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class LargePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"


class StandardTitlePagination(PageNumberPagination):
    page_size = 33
    page_size_query_param = "page_size"


class StandardEntryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
