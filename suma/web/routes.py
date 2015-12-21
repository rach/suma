from paste.deploy.converters import asbool


def includeme(config):

    if not asbool(config.registry.settings.get('storage.s3', False)):
        storage_url = config.registry.settings['storage.local.base_url']
        storage_path = config.registry.settings['storage.local.base_path']
        config.add_static_view(storage_url.replace('/', ''), path=storage_path)

    config.add_route('links', '/*traverse',
                     factory='suma.web.resources.LinkFactory')
