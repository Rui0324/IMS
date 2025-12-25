from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def api_response(data=None, msg='success', code=0, status_code=status.HTTP_200_OK):
    return Response({'code': code, 'msg': msg, 'data': data}, status=status_code)


class StandardResultsSetPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'pageSize'
    page_size = 10
    max_page_size = 100


class ApiResponseMixin:
    """
    Mixin to wrap CRUD responses in the unified {code, msg, data} envelope
    with pagination shape aligned to /specs/api_contract.md.
    """

    pagination_class = StandardResultsSetPagination

    def success(self, data=None, msg='success', status_code=status.HTTP_200_OK, code=0):
        return api_response(data=data, msg=msg, code=code, status_code=status_code)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)
        if page is not None:
            paginator = self.paginator
            return self.success(
                {
                    'list': serializer.data,
                    'total': paginator.page.paginator.count,
                    'page': paginator.page.number,
                    'pageSize': paginator.get_page_size(request),
                }
            )
        return self.success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.success(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.success(serializer.data, status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return self.success(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.success({})
