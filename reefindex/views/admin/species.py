from pyramid.view import view_config

from ... import model


@view_config(route_name='edit_species', renderer='admin/edit_species.mako')
def edit_species(request):
    id = request.matchdict['id']
    species = model.Species.get(id)
    return {'species': species}
