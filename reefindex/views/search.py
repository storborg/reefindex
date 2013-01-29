import math

from pyramid.view import view_config
from webhelpers.paginate import PageURL_WebOb, Page

from .. import model


def paginated_result(request, q):
    page_url = PageURL_WebOb(request)
    page_num = int(request.params.get('page') or 1)
    per_page = int(request.params.get('per_page') or 5)

    offset = (page_num - 1) * per_page
    limit = per_page

    q = q.limit(limit).offset(offset)
    result = q.execute()

    return Page(list(result),
                page=page_num,
                items_per_page=per_page,
                item_count=result.count,
                presliced_list=True,
                url=page_url)


@view_config(route_name='search', renderer='list.mako')
def search(request):
    phrase = request.params.get('q')

    es_client = request.registry.es_client

    q = es_client.query(model.Species, q=phrase)

    upper = request.params.get('size_upper')
    lower = request.params.get('size_lower')
    if upper:
        q = q.filter_value_upper('size_max', upper)
    if lower:
        q = q.filter_value_lower('size_max', lower)

    page = paginated_result(request, q)
    return {'page': page}
