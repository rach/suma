from zope.interface import Interface


class IHashIdService(Interface):

    def encode(self, primary_id, secondary_id=None):
        pass

    def decode(self, short_id):
        pass
