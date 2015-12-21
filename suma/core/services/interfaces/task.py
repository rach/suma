from zope.interface import Interface


class ITaskService(Interface):
    def add_click(self, link_id, ip=None, referer=None):
        pass

    def get_link_data(self, link_id):
        pass
