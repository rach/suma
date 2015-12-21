from pyramid.config import Configurator


def get_config(global_config, **settings):
    """
    Control configurations state
    """
    merged_settings = {}
    merged_settings.update(global_config)
    merged_settings.update(settings)
    config = Configurator(settings=merged_settings)
    config.include('suma.api.settings.extension')
    config.include('suma.api.settings.logger')
    config.include('suma.api.settings.service')
    config.include('suma.api.routes')
    config.include('suma.api.settings.adapter')
    config.include('suma.api.settings.celery')
    config.scan('suma.api')
    return config
