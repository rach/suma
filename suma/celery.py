from __future__ import absolute_import
from optparse import make_option
from celery import signals, Celery
from pyramid.paster import bootstrap, get_appsettings
from sqlalchemy import create_engine
from celery import Task
from celery.loaders.base import BaseLoader
from suma.core.models.meta import create_dbsession
from paste.deploy.converters import aslist, asbool

celery = Celery()

celery.user_options['preload'].add(
    make_option(
        '-i', '--ini',
        default=None,
        help='Paste ini configuration file.'),
)


class INILoader(BaseLoader):

    def __init__(self, app, **kwargs):
        self.celery_conf = kwargs.pop('ini_file')

        super(INILoader, self).__init__(app, **kwargs)

    def read_configuration(self, fail_silently=True):
        config_dict = {}

        for key, value in get_appsettings(self.celery_conf).items():
            if key.lower().startswith('celery.'):
                config_dict[key[7:].upper()] = value

        config_dict['CELERY_IMPORTS'] = [
           'suma.core.tasks',
        ]
        return config_dict


@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    ini_location = options['ini']

    if ini_location is None:
        print('You must provide the paste --ini argument')
        exit(-1)

    loader = INILoader(celery, ini_file=ini_location)
    celery_config = loader.read_configuration()
    celery.config_from_object(celery_config)
    registry = bootstrap(ini_location)['registry']
    celery.conf.update({'pyramid.registry': registry})


class SumaTask(Task):
    abstract = True
    _dbsession = None
    _registry = None
    _services = None
    _flags = None

    @property
    def dbsession(self):
        if self._dbsession is None:
            engine = create_engine(self.registry.settings['sqlalchemy.url'])
            self._dbsession = create_dbsession(engine)
        return self._dbsession

    @property
    def registry(self):
        if self._registry is None:
            self._registry = celery.conf['pyramid.registry']
        return self._registry

    @property
    def flags(self):
        if self._flags is None:
            flags = aslist(self.registry.settings.get('suma.tasks',[]))
            self._flags = flags
        return self._flags

    @property
    def services(self):
        #circular imports otherwise
        from suma.core.services import (
            LinkService,
            HashIdService,
            ScreenshotService,
            LocalFileService,
            S3FileService,
            StatService
        )
        if self._services is None:
            services_dict = {}
            secret = self.registry.settings['hashid.secret']
            if asbool(self.registry.settings.get('storage.s3', False)):
                services_dict['file'] = S3FileService(
                    self.registry.settings['storage.s3.base_url'],
                    self.registry.settings['storage.s3.bucket_name'],
                    self.registry.settings['storage.s3.access_key'],
                    self.registry.settings['storage.s3.secret_key'],
                )
            else:
                services_dict['file'] = LocalFileService(
                    self.registry.settings['storage.local.base_url'],
                    self.registry.settings['storage.local.base_path'],
                )
            services_dict['hashid'] = HashIdService(secret)
            services_dict['screenshot'] = ScreenshotService()
            services_dict['stat'] = StatService(self.dbsession)
            services_dict['link'] = LinkService(self.dbsession,
                                                services_dict['hashid'])
            self._services = type('Services', (), services_dict)
        return self._services

celery.Task = SumaTask
task = celery.task
