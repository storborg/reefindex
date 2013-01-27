from pyramid.view import notfound_view_config


@notfound_view_config(renderer='notfound.mako')
def notfound(request):
    return {}
