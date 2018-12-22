from rest_framework.pagination import PageNumberPagination


class FilePagination(PageNumberPagination):
    page_size = 10
    max_page_size = 5
    page_query_param = "page"