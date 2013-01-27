from pyramid.view import view_config


@view_config(route_name='species', renderer='species.mako')
def species(request):
    id = request.matchdict['id']
    es_client = request.registry.es_client
    thing = es_client.get(('Species', id))
    return {'species': thing}
