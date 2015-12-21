from suma.core.services.interfaces import IScreenshotService
from zope.interface import implementer
from selenium import webdriver
from structlog import get_logger
log = get_logger()


@implementer(IScreenshotService)
class ScreenshotService(object):

    def capture(self, url, width, height):
        # TODO we need a more efficiant way to avoid recreating driver everytimes
        driver = webdriver.PhantomJS()
        try:
            driver.set_window_size(width, height)
            driver.get(url)
            return driver.get_screenshot_as_png(), driver.page_source
        finally:
            driver.quit()
