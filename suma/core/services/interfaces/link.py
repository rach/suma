from zope.interface import Interface


class ILinkService(Interface):

    def create_link(self, url, user_id=None):
        pass

    def get_link_by_id_or_hashid(self, id_or_hashid):
        pass

    def get_link_by_url(self, url, user_id=None):
        pass

    def get_link_by_id(self, id):
        pass

    def get_link_by_hashid(self, hashid):
        pass

    def ban_url(self, url, mode='url'):
        pass
