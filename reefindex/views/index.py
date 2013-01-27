from pyramid.view import view_config

from .. import model


@view_config(route_name='index', renderer='list.mako')
def index(request):
    es_client = request.registry.es_client
    q = es_client.query(model.Species).order_by('_id', desc=True)
    results = q.all()

    return {'results': results}
