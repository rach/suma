from pyramid.renderers import JSON
import datetime
from suma.core.models.meta import EnumSymbol


def enum_adapter(obj, request):
    return obj.value


def datetime_adapter(obj, request):
    return obj.isoformat()


def includeme(config):
    json_renderer = JSON()
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    json_renderer.add_adapter(EnumSymbol, enum_adapter)
    config.add_renderer('json', json_renderer)

