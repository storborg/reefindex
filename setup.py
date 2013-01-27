from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_es',

    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='reefindex',
      version='0.1',
      description='A demo app to index reef creatures',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      keywords='pyramid pyramid_es elasticsearch reef science biology',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='reefindex',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = reefindex:main
      [console_scripts]
      initialize_reefindex_db = reefindex.scripts.initializedb:main
      """,
      )
