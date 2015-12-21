from pyramid.events import BeforeRender, NewRequest, ContextFound
from pyramid.events import subscriber
from structlog import get_logger
import uuid


log = get_logger()


@subscriber(NewRequest)
def add_logger_request_id(event):
    log.new(request_id=uuid.uuid4())
