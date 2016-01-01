from pyramid.config import Configurator


def get_config(global_config, **settings):
    """
    Control configurations state
    """
    merged_settings = {}
    merged_settings.update(global_config)
    merged_settings.update(settings)
    config = Configurator(settings=merged_settings)
    config.include('suma.web.settings.extension')
    config.include('suma.web.settings.logger')
    config.include('suma.web.settings.service')
    config.include('suma.web.routes')
    config.include('suma.web.settings.adapter')
    config.scan('suma.web')
    return config
