import os.path

from pyramid.config import Configurator
from pyramid.events import BeforeRender

from sqlalchemy import engine_from_config

from . import model, helpers
from .model import DBSession, Base

here = os.path.dirname(os.path.abspath(__file__))


def add_renderer_globals(event):
    event['h'] = helpers


def main(global_config, **settings):
    """
    Set up the main application.
    """
    settings['mako.directories'] = os.path.join(here, 'templates')

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('index', '/')
    config.add_route('search', '/search')
    config.add_route('species', '/species/{id}')

    config.add_route('edit_species', '/species/{id}/edit')

    config.add_subscriber(add_renderer_globals, BeforeRender)

    config.scan('.views')

    return config.make_wsgi_app()
