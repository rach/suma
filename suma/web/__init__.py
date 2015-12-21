from suma.web.config import get_config


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = get_config(global_config, **settings)
    return config.make_wsgi_app()
