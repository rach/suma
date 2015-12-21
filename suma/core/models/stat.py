from sqlalchemy import (
    Column,
    Unicode,
    String,
    BigInteger,
    ForeignKey,
    or_
)
from sqlalchemy.dialects.postgresql import INET
from .link import Link
from sqlalchemy.orm import relationship, backref
from suma.core.models.meta import (
    Base,
    CreatedColumn
)


class Stat(Base, CreatedColumn):
    link_id = Column(ForeignKey(Link.id), nullable=False)
    link = relationship(Link, backref=backref('stats'))
    referer = Column(Unicode)
    ip = Column(INET)

# The models belows, are denormalized models from Stat for quick lookup


class ClickCounter(Base):
    id = Column(ForeignKey(Link.id), primary_key=True, nullable=False)
    link = relationship(Link, backref=backref('_clicks', uselist=False, lazy='joined'))
    counter = Column(BigInteger, default=1)
