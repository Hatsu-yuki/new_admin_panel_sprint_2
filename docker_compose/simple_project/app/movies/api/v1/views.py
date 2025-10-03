from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import FilmWork


class MoviesListApi(BaseListView):
    model = FilmWork
    http_method_names = ['get']  # Список методов, которые реализует обработчик
    paginate_by = 50

    def get_queryset(self):
        return FilmWork.objects.all().values("id", "title", "description",
                                             "creation_date", "rating",
                                             "type")
    def get_context_data(self, *, object_list=None, **kwargs):

        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
