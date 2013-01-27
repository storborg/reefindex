from pyramid.view import view_config

from .. import model


@view_config(route_name='search', renderer='list.mako')
def search(request):
    phrase = request.params.get('q')

    es_client = request.registry.es_client
    q = es_client.query(model.Species, q=phrase)
    results = q.all()

    return {'results': results}
