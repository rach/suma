from suma.core.services import LinkService, HashIdService, StatService
from hashlib import sha1
from sqlalchemy.exc import IntegrityError
import pytest


@pytest.fixture
def link_svc(db_session, hashid_svc):
    return LinkService(db_session, hashid_svc)


@pytest.fixture
def hashid_svc():
    return HashIdService('secret')

@pytest.fixture
def stat_svc(db_session):
    return StatService(db_session)
