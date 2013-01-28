from pyramid.view import view_config

from .. import model
from .search import paginated_result


@view_config(route_name='index', renderer='list.mako')
def index(request):
    es_client = request.registry.es_client
    q = es_client.query(model.Species).order_by('_id', desc=True)

    page = paginated_result(request, q)

    return {'results': page}
