import pytest
from sqlalchemy import create_engine
from suma.core.models.meta import create_dbsession, Base
import zope.sqlalchemy
from pyramid import testing
from pyramid_services import find_service
from zope.interface.adapter import AdapterRegistry
import types


@pytest.fixture(scope='session')
def db(request):
    """Session-scoped sqlalchemy database connection"""
    engine = create_engine('postgresql://suma@/suma_test')
    dbsession = create_dbsession(engine)
    zope.sqlalchemy.register(dbsession)
    # we drop before to be sure we didn't leave the previous state unclean
    Base.metadata.drop_all()
    Base.metadata.create_all()
    dbsession.registry.clear()
    request.addfinalizer(Base.metadata.drop_all)
    return dbsession


@pytest.fixture
def db_session(request, db):
    """Function-scoped sqlalchemy database session"""
    from transaction import abort
    trans = db.connection().begin()
    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)
    return db



@pytest.fixture
def config(request):
    config = testing.setUp()
    config.registry.settings['storage.local.base_url'] = '/tmp'
    config.registry.settings['storage.local.base_path'] = '/storage'
    config.include('pyramid_services')
    request.addfinalizer(testing.tearDown)
    return config

@pytest.fixture
def dummy_request(request, config):
    req = testing.DummyRequest()
    req.find_service = types.MethodType(find_service, req)
    req.service_cache = AdapterRegistry()
    return req
