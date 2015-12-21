from suma.core.services.interfaces import ITaskService
from suma.core import tasks
from zope.interface import implementer
from structlog import get_logger
from types import IntType, LongType
log = get_logger()


@implementer(ITaskService)
class TaskService(object):
    def add_click(self, link_id, ip=None, referer=None):
        assert type(link_id) in [IntType, LongType], "link_id is not an integer: %r" % link_id
        tasks.add_click_task.apply_async((link_id, ip, referer), serializer='json')

    def get_link_data(self, link_id):
        assert type(link_id) in [IntType, LongType], "link_id is not an integer: %r" % link_id
        tasks.get_link_data_task.apply_async((link_id, ), serializer='json')
