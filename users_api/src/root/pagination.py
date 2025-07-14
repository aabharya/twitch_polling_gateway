from collections import OrderedDict

from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_data(self, data):
        return OrderedDict(
            [
                ('limit', self.limit),
                ('offset', self.offset),
                ('count', self.count),
                ('next', self.get_next_link()),
                ('previous', self.get_previous_link()),
                ('results', data),
            ]
        )

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ('limit', self.limit),
                    ('offset', self.offset),
                    ('count', self.count),
                    ('next', self.get_next_link()),
                    ('previous', self.get_previous_link()),
                    ('results', data),
                ]
            )
        )


def get_paginated_response(*, serializer_class, queryset, request, view):
    paginator = LimitOffsetPagination()

    page = paginator.paginate_queryset(queryset, request, view=view)
    serializer_context = {'request': request}
    if page is not None:
        serializer = serializer_class(page, many=True, context=serializer_context)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True, context=serializer_context)

    return Response(data=serializer.data, status=status.HTTP_200_OK)
