from suma.api.resources import LinkResource, LinkFactory
from suma.core.models import Link
from suma.core.services.interfaces import (
    ITaskService,
    ILinkService,
    IFileService
)
from zope.interface import implementer
import pytest
import os


@implementer(IFileService)
class FakeFileService(object):

    def create(self, data, filename, folder):
        return os.path.join(folder, filename)

    def url(self, filename):
        return 'http://localhost/' + filename


@implementer(ILinkService)
class FakeLinkService(object):
    def __init__(self):
        self._link = Link(
            id=1, url='https://google.com', hashid='1234',
            meta={"title": "TEST", "screenshot": "screenshots/1234.png"}
        )
        self._created = True

    def create_link(self, url, user_id=None):
        return self._link, True

    def get_link_by_id_or_hashid(self, id_or_hashid):
        if id_or_hashid in [1, '1234']:
            return self._link
        return None

    def get_link_by_url(self, url, user_id=None):
        if url == 'https://google.com':
            return self._link
        return None

    def get_link_by_id(self, id):
        if id == 1:
            return self._link
        return None

    def get_link_by_hashid(self, hashid):
        if hashid == '1234':
            return self._link
        return None

    def ban_url(self, url, mode='url'):
        pass


@implementer(ITaskService)
class FakeTaskService(object):
    def add_click(self, link_id, ip=None, referer=None):
        pass

    def get_link_data(self, link_id):
        pass


@pytest.fixture
def link(db_session):
    link = Link(hashid='1234', url='http://google.com')
    db_session.add(link)
    db_session.flush()
    return link


@pytest.fixture
def link_resource(link):
    return LinkResource(link)


@pytest.fixture
def fake_task_service(config):
    service = FakeTaskService()
    config.register_service(service, name='task')
    return service


@pytest.fixture
def fake_link_service(config):
    service = FakeLinkService()
    config.register_service(service, name='link')
    return service


@pytest.fixture
def fake_file_service(config):
    service = FakeFileService()
    config.register_service(service, name='file')
    return service

@pytest.fixture(autouse=True)
def routes(config):
    config.include('suma.api.routes')


def test_create_link_api_view(dummy_request, fake_link_service,
                              fake_task_service, fake_file_service):
    from suma.api.views import LinkView
    dummy_request.method = 'POST'
    dummy_request.post = '{"url": "http://google.com"}'
    dummy_request.json_body = {"url": "http://google.com"}
    view = LinkView(LinkFactory(dummy_request), dummy_request)
    response_obj = view.create_link()
    assert dummy_request.response.status_code == 201
    assert response_obj["data"]["id"] == 1
    assert response_obj["data"]["attributes"]["hashid"] == '1234'


def test_create_link_api_view_fail_validation(dummy_request, fake_link_service,
                                              fake_task_service, fake_file_service):
    from suma.api.views import LinkView
    dummy_request.method = 'POST'
    dummy_request.post = '{"unknown": "http://google.com"}'
    dummy_request.json_body = {"unknown": "http://google.com"}
    view = LinkView(LinkFactory(dummy_request), dummy_request)
    response = view.create_link()
    assert response.status_code == 400


def test_ban_link_api_view(db_session, dummy_request,
                           fake_link_service, fake_task_service, fake_file_service):
    from suma.api.views import LinkView
    l = Link(url="http://google.com", hashid='1234')
    db_session.add(l)
    db_session.flush()
    dummy_request.method = 'POST'
    dummy_request.post = '{"mode": "url"}'
    dummy_request.json_body = {"mode": "url"}
    view = LinkView(LinkResource(l), dummy_request)
    response = view.ban()
    assert response.status_code == 201
