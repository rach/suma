from zope.interface import Interface


class IStatService(Interface):
    def add_click(self, link_id, ip=None, referer=None):
        pass

    def get_counter_by_link_id(self, link_id):
        pass
