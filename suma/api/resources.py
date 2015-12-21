from suma.common.resources.base import ResourceWrapper


class LinkFactory(object):

    def __init__(self, request):
        self.request = request

    def __getitem__(self, key):
        svc = self.request.find_service(name='link')
        link = svc.get_link_by_id_or_hashid(key)
        if link:
            return LinkResource(link)
        raise KeyError(key)

    def unwrap(self):
        return None


class LinkResource(ResourceWrapper):
    __name__ = 'LinkResource'
    __parent__ = LinkFactory

    def __getitem__(self, key):
        raise KeyError(key)
