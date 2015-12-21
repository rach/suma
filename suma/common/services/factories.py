from suma.core.services import (
    LinkService,
    HashIdService,
    TaskService,
    S3FileService,
    LocalFileService
)
from paste.deploy.converters import asbool


def link_service_factory(context, request):
    dbsession = request.find_service(name='db', context=context)
    hashid = request.find_service(name='hashid', context=context)
    return LinkService(
        dbsession=dbsession,
        hashid=hashid,
    )


def hashid_service_factory(context, request):
    hashid_secret = request.registry.settings.get('hashid.secret')
    return HashIdService(
        secret=hashid_secret
    )


def task_service_factory(context, request):
    return TaskService()


def file_service_factory(context, request):
    if asbool(request.registry.settings.get('storage.s3', False)):
        return S3FileService(
            request.registry.settings['storage.s3.base_url'],
            request.registry.settings['storage.s3.bucket_name'],
            request.registry.settings['storage.s3.access_key'],
            request.registry.settings['storage.s3.secret_key'],
        )
    return LocalFileService(
        request.registry.settings['storage.local.base_url'],
        request.registry.settings['storage.local.base_path'],
    )
