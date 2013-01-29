from pyramid.paster import get_app

application = get_app('/var/sw/reefindex/production.ini', 'main')
