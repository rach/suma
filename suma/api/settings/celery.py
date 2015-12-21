from suma.celery import celery


def includeme(config):
    config_dict = {}
    for key, value in config.registry.settings.items():
        if key.lower().startswith('celery.'):
            config_dict[key[7:].upper()] = value
    celery.config_from_object(config_dict)
