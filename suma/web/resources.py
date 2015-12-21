from suma.common.resources import ResourceWrapper


class LinkFactory(object):

    def __init__(self, request):
        self.request = request
        self.svc = request.find_service(name='link', context=None)

    def __getitem__(self, key):
        link = self.svc.get_link_by_hashid(key)
        if link and not link.is_banned:
            return LinkResource(link)
        raise KeyError(key)


class LinkResource(ResourceWrapper):

    def __getitem__(self, key):
        raise KeyError(key)
