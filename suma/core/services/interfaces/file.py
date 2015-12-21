
from zope.interface import Interface


class IFileService(Interface):

    def create(self, data, filename, folder):
        pass

    def url(self, filename):
        pass
