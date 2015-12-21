from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import event, DDL
from sqlalchemy import (
    Column,
    Integer
)
import re


_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')


def _camel_to_snake(s):
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return _camel_to_snake(cls.__name__)

    __table_args__ = {'schema': 'suma'}

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)

event.listen(Base.metadata, 'before_create',
             DDL("CREATE SCHEMA IF NOT EXISTS suma"))


def create_dbsession(engine):
    dbsession = scoped_session(sessionmaker())
    dbsession.configure(bind=engine)
    Base.metadata.bind = engine
    return dbsession
