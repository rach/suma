

def includeme(config):
    config.include('pyramid_tm')
    config.include('pyramid_services')
    config.include('pyramid_exclog')
