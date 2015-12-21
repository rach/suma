from suma.core.services.interfaces import IFileService
from depot.manager import DepotManager
from zope.interface import implementer
from structlog import get_logger
log = get_logger()
from pyramid_storage.local import LocalFileStorage
from pyramid_storage.s3 import S3FileStorage
from cStringIO import StringIO


@implementer(IFileService)
class LocalFileService(object):
    def __init__(self, base_url, base_path):
        suffix = ''
        if not base_url.endswith('/'):
            suffix = '/'
        self.storage = LocalFileStorage(base_path, base_url + suffix)

    def create(self, data, filename, folder):
        output = StringIO(data)
        return self.storage.save_file(output, filename, folder)  # return final filename

    def url(self, filename):
        return self.storage.url(filename)


@implementer(IFileService)
class S3FileService(LocalFileService):
    def __init__(self, base_url, bucket_name, access_key, secret_key):
        suffix = ''
        if not base_url.endswith('/'):
            suffix = '/'
        self.storage = S3FileStorage(
            bucket_name=bucket_name,
            base_url=base_url + suffix,
            access_key=access_key,
            secret_key=secret_key
        )
