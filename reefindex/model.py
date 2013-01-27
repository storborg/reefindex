from sqlalchemy import Column, ForeignKey, types, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid_es.mixin import ElasticMixin, ESMapping, ESField, ESString


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class _Base(object):

    @classmethod
    def get(cls, id):
        return DBSession.query(cls).get(id)

    @classmethod
    def find_or_create(cls, **kwargs):
        try:
            obj = DBSession.query(cls).filter_by(**kwargs).one()
        except NoResultFound:
            obj = cls(**kwargs)
            DBSession.add(obj)
        return obj


Base = declarative_base(cls=_Base)


class Order(Base, ElasticMixin):
    __tablename__ = 'orders'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(types.Integer, primary_key=True)
    latin = Column(types.Unicode, unique=True, nullable=False)
    name = Column(types.Unicode, unique=True, nullable=True)
    description = Column(types.UnicodeText, nullable=True)

    @classmethod
    def elastic_mapping(cls):
        return ESMapping(
            analyzer='content',
            properties=ESMapping(
                ESString('latin', analyzer='lowercase', boost=2.0),
                ESString('name', analyzer='lowercase', boost=5.0),
                ESString('description')))


class Family(Base, ElasticMixin):
    __tablename__ = 'families'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    __elastic_parent__ = ('Order', 'order_id')

    id = Column(types.Integer, primary_key=True)
    latin = Column(types.Unicode, unique=True, nullable=False)
    name = Column(types.Unicode, unique=True, nullable=True)
    description = Column(types.UnicodeText, nullable=True)

    order_id = Column(None, ForeignKey('orders.id'), nullable=False)
    order = orm.relationship('Order')

    @classmethod
    def elastic_mapping(cls):
        return ESMapping(
            analyzer='content',
            properties=ESMapping(
                ESString('latin', analyzer='lowercase', boost=2.0),
                ESString('name', analyzer='lowercase', boost=5.0),
                ESString('description')))


class Genus(Base, ElasticMixin):
    __tablename__ = 'genera'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    __elastic_parent__ = ('Family', 'family_id')

    id = Column(types.Integer, primary_key=True)
    latin = Column(types.Unicode, unique=True, nullable=False)
    name = Column(types.Unicode, unique=True, nullable=True)
    description = Column(types.UnicodeText, nullable=True)

    family_id = Column(None, ForeignKey('families.id'), nullable=False)
    family = orm.relationship('Family')

    @classmethod
    def elastic_mapping(cls):
        return ESMapping(
            analyzer='content',
            properties=ESMapping(
                ESString('latin', analyzer='lowercase', boost=2.0),
                ESString('name', analyzer='lowercase', boost=5.0),
                ESString('description')))


class Species(Base, ElasticMixin):
    __tablename__ = 'species'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    __elastic_parent__ = ('Genus', 'genus_id')

    id = Column(types.Integer, primary_key=True)
    latin = Column(types.Unicode, unique=True, nullable=False)
    name = Column(types.Unicode, unique=True, nullable=True)

    description = Column(types.UnicodeText, nullable=True)
    range = Column(types.UnicodeText, nullable=True)
    diet = Column(types.UnicodeText, nullable=True)
    breeding = Column(types.UnicodeText, nullable=True)
    ethics = Column(types.UnicodeText, nullable=True)

    size_min = Column(types.Integer, nullable=True)
    size_max = Column(types.Integer, nullable=True)

    genus_id = Column(None, ForeignKey('genera.id'), nullable=False)
    genus = orm.relationship('Genus')

    @property
    def genus_latin(self):
        return self.genus.latin

    @property
    def family_latin(self):
        return self.genus.family.latin

    @property
    def order_latin(self):
        return self.genus.family.order.latin

    @classmethod
    def elastic_mapping(cls):
        return ESMapping(
            analyzer='content',
            properties=ESMapping(
                ESString('latin', analyzer='lowercase', boost=2.0),
                ESString('name', analyzer='lowercase', boost=10.0),

                ESString('description'),
                ESString('range'),
                ESString('diet'),
                ESString('breeding'),
                ESString('ethics'),

                ESString('genus_latin'),
                ESString('family_latin'),
                ESString('order_latin'),

                ESField('size_min'),
                ESField('size_max')))
