from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import (
    HTTPMovedPermanently,
    HTTPOk,
    HTTPNotFound,
    HTTPFound
)
from suma.web.resources import LinkResource


@view_defaults(route_name='links')
class LinkView():

    def __init__(self, context, request):
        self.context = context
        self.link = context.unwrap()
        self.request = request
        self.task = request.find_service(name='task')
        self.file = request.find_service(name='file')

    @view_config(context=LinkResource, request_method='GET')
    def get(self):
        self.task.add_click(
            self.link.id,
            self.request.remote_addr,
            self.request.referer
        )
        return HTTPMovedPermanently(self.link.url)

    @view_config(context=LinkResource, name='screenshot')
    def screenshot(self):
        screenshot = self.link.meta.get('screenshot', None)
        if screenshot:
            return HTTPFound(location=self.file.url(screenshot))
        return HTTPNotFound()
