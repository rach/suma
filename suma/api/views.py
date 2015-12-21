from pyramid.view import view_config, view_defaults
from suma.api.schemas import LinkSchema, BanSchema, BanLinkSchema
from suma.api.resources import LinkResource
from schematics.exceptions import ModelValidationError, ModelConversionError
from suma.api import serializers
from pyramid.httpexceptions import HTTPBadRequest, HTTPOk, HTTPCreated, HTTPNoContent
import json

from pyramid.view import (
    notfound_view_config
)


@notfound_view_config(renderer='json')
def notfound(request):
    request.response.status = 404
    return {}

@view_defaults(route_name='links', renderer='json')
class LinkView():

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.link = context.unwrap()
        self.response = request.response
        self.link_svc = request.find_service(name='link')
        self.task = request.find_service(name='task')

    @view_config(request_method='POST')
    def create_link(self):
        try:
            schema = LinkSchema(self.request.json_body)  # Can raise ModelConversionError
            schema.validate()  # Can raise ModelValidationError
            link, created = self.link_svc.create_link(schema.url, schema.user_id)
            if created:
                self.task.get_link_data(link.id, )
                self.response.status_code = 201
            return serializers.serialize_create_link(self.request, link)
        except (ModelConversionError, ModelValidationError), e:
            return HTTPBadRequest(json.dumps(e.messages))
        except ValueError, e:
            # Json badly formated
            return HTTPBadRequest(json.dumps(e.message))

    @view_config(context=LinkResource, request_method='GET')
    def get_link(self):
        return serializers.serialize_get_link(self.request, self.context.unwrap())

    @view_config(context=LinkResource, request_method='GET', name='text', renderer='string')
    def get_link_text(self):
        text = self.link.meta.get('text', None)
        if not text:
            return HTTPNoContent()
        return text

    @view_config(context=LinkResource, request_method='GET', name='html')
    def get_link_text(self):
        html = self.link.meta.get('html', None)
        if not html:
            return HTTPNoContent()
        return HTTPOk(body=html)

    @view_config(context=LinkResource, name='refresh')
    def refresh_link(self):
        self.task.get_link_data(self.link.id, )
        return HTTPOk('link queued to refresh meta')
 
    @view_config(context=LinkResource, request_method='POST', name='ban')
    def ban(self):
        try:
            schema = BanLinkSchema(self.request.json_body)  # Can raise ModelConversionError
            schema.validate()  # Can raise ModelValidationError
            self.link_svc.ban_url(self.link.url, schema.mode)
            return HTTPCreated("link's %s banned" % schema.mode)
        except (ModelConversionError, ModelValidationError), e:
            return HTTPBadRequest(json.dumps(e.messages))
        except ValueError, e:
            # Json badly formated
            return HTTPBadRequest(json.dumps(e.message))


# TODO: Rewrite to void code duplicate but slightly different as the url is pulled from schema

@view_config(route_name='ban', request_method='POST')
def ban_api(request):
    link_svc = request.find_service(name='link')
    try:
        schema = BanSchema(request.json_body)  # Can raise ModelConversionError
        schema.validate()  # Can raise ModelValidationError
        link_svc.ban_url(schema.url, schema.mode)
        return HTTPCreated("link's %s banned" % schema.mode)
    except (ModelConversionError, ModelValidationError), e:
        return HTTPBadRequest(json.dumps(e.messages))
    except ValueError, e:
        # Json badly formated
        return HTTPBadRequest(json.dumps(e.message))
