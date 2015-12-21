from sqlalchemy import (
    Column,
    Unicode,
    String,
    BigInteger,
    UniqueConstraint,
    or_,
    Index
)

from suma.core.models.meta import (
    Base,
    DeclEnum,
    TimestampColumns
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import exists
from sqlalchemy.orm import column_property
from sqlalchemy.ext.mutable import MutableDict
from urlparse import urlparse
from hashlib import sha1


class BlockingType(DeclEnum):
    url = "url", "Url"
    netloc = "netloc", "Netloc"
    path = "path", "Path"


class BlockedLink (Base):
    url = Column('url', Unicode, nullable=False)  # this is there more for readability
    hash = Column(String, index=True, unique=True, nullable=False)
    type = Column(BlockingType.db_type(), nullable=False)


class Link(Base, TimestampColumns):
    hashid = Column(String, index=True, unique=True, nullable=False)
    _url = Column('url', Unicode, index=True, nullable=False)
    user_id = Column(BigInteger)
    _hash = Column('hash', String, index=True, nullable=False)
    _hash_netloc = Column('hash_netloc', String, nullable=False)
    _hash_path = Column('hash_path', String, nullable=False)
    meta = Column(MutableDict.as_mutable(JSONB), default={})
    __table_args__ = (
        Index('unique_url_and_user_id', _url, user_id, unique=True,
              postgresql_where=(user_id != None)),
        Index('unique_url_and_user_id_is_null', 'url', unique=True,
              postgresql_where=(user_id == None))
    )

    is_banned = column_property(
        exists().where(
            or_(
                BlockedLink.hash.in_([_hash, _hash_netloc, _hash_path])
            )
        )
    )

    @property
    def clicks(self):
        if self._clicks:
            return self._clicks.counter
        return 0
    
    @hybrid_property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
        self._hash, self._hash_netloc, self._hash_path = create_url_hashes(value)


def create_url_hashes(url):
    parsed = urlparse(url)
    return (
        sha1(url).hexdigest(),
        sha1(parsed.netloc).hexdigest(),
        sha1(parsed.netloc + parsed.path).hexdigest()
    )
