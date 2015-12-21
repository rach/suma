from suma.web.resources import LinkResource
from suma.core.models import Link
from suma.core.services.interfaces import ITaskService, IFileService
from zope.interface import implementer
import pytest
import os


@implementer(IFileService)
class FakeFileService(object):

    def create(self, data, filename, folder):
        return os.path.join(folder, filename)

    def url(self, filename):
        return 'http://localhost/' + filename


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
def fake_file_service(config):
    service = FakeFileService()
    config.register_service(service, name='file')
    return service


@pytest.fixture(autouse=True)
def routes(config):
    config.include('suma.web.routes')


def test_get_link_view(dummy_request, link_resource, fake_task_service, fake_file_service):
    from suma.web.views import LinkView
    dummy_request.remote_addr = '127.0.0.1'
    dummy_request.referer = 'http://test.com'
    view = LinkView(link_resource, dummy_request)
    response = view.get()
    assert response.status_code == 301
    assert response.headers.get('Location') == 'http://google.com'
