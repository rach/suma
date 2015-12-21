from schematics.models import Model
from schematics.types import URLType, LongType, StringType


_choices = ['url', 'netloc', 'path']

class LinkSchema(Model):
    url = URLType(required=True)
    user_id = LongType(min_value=0, required=False)

class BanSchema(Model):
    url = URLType(required=True)
    mode = StringType(choices=_choices, default='url', required=False)

class BanLinkSchema(Model):
    mode = StringType(choices=_choices, default='url', required=False)
