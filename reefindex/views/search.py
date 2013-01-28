from pyramid.view import view_config
from webhelpers.paginate import PageURL_WebOb, Page

from .. import model


def paginated_result(request, q, page_num=1):
    page_url = PageURL_WebOb(request)
    return Page(list(q.all()), page_num, url=page_url, items_per_page=50)


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
    return {'results': page}
