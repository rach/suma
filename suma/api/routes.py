

def includeme(config):
    config.add_route('links', '/links*traverse',
                     factory='suma.api.resources.LinkFactory')
    config.add_route('ban', '/ban')
