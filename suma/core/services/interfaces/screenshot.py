from zope.interface import Interface


class IScreenshotService(Interface):
    def capture(self, url, width, height):
        pass
