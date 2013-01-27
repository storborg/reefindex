import logging

import os
import os.path
import sys
import json

import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import get_appsettings, setup_logging
from pyramid_es import client_from_config

from .. import model
from ..model import DBSession, Base

log = logging.getLogger(__name__)

here = os.path.dirname(os.path.abspath(__file__))
sampledir = os.path.join(os.path.dirname(here), 'samples')


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def add_sample(es_client, doc):
    order = model.Order.find_or_create(latin=doc.pop('order'))

    family = model.Family.find_or_create(latin=doc.pop('family'))
    if family.order:
        assert family.order == order
    else:
        family.order = order

    genus = model.Genus.find_or_create(latin=doc.pop('genus'))
    if genus.family:
        assert genus.family == family
    else:
        genus.family = family

    species = model.Species(
        genus=genus,
        **doc)
    DBSession.add(species)
    DBSession.flush()

    es_client.index_object(order)
    es_client.index_object(family)
    es_client.index_object(genus)
    es_client.index_object(species)


def add_samples(es_client):
    for filename in os.listdir(sampledir):
        if filename.endswith('.json'):
            log.info("Loading %r" % filename)
            with open(os.path.join(sampledir, filename)) as f:
                doc = json.load(f)
                add_sample(es_client, doc)


def reset_sqlite(sa_url):
    if sa_url.startswith('sqlite://') and sa_url != 'sqlite:///:memory:':
        dbfile = sa_url[10:]
        if os.path.exists(dbfile):
            os.remove(dbfile)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    reset_sqlite(settings['sqlalchemy.url'])

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    es_client = client_from_config(settings, 'elastic.')
    es_client.ensure_index(recreate=True)
    es_client.ensure_all_mappings(Base, recreate=True)

    with transaction.manager:
        add_samples(es_client)
