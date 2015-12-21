
def serialize_link(request, link):
    file = request.find_service(name='file')
    screenshot = link.meta.get('screenshot', None)
    if screenshot:
        screenshot = file.url(screenshot)
    return {
        "data": {
            "type": "links",
            "id": link.id,
            "attributes": {
                "hashid": link.hashid,
                "url": link.url,
                "banned": link.is_banned,
                "clicks": link.clicks,
                "screenshot": screenshot,
                "title": link.meta.get('title', None),
                "created": link.created,
                "updated": link.updated
            },
            "actions": {
                "html": {
                    "links": {
                        "related": request.route_url('links', traverse='/%s/%s' % (link.id, 'html'))
                    }
                },
                "text": {
                    "links": {
                        "related": request.route_url('links', traverse='/%s/%s' % (link.id, 'text'))
                    }
                },
                "ban": {
                    "links": {
                        "related": request.route_url('links', traverse='/%s/%s' % (link.id, 'ban'))
                    }
                },
                "refresh": {
                    "links": {
                        "related": request.route_url('links', traverse='/%s/%s' % (link.id, 'refresh'))
                    }
                },
            }
        }
    }

def serialize_create_link(request, link):
    val = serialize_link(request, link)
    val["data"]["links"] = {"self": request.route_url('links',  traverse='/%s' % (link.id,))}
    return val

def serialize_get_link(request, link):
    val = serialize_link(request, link)
    val["links"] = {"self": request.route_url('links', traverse='/%s' % (link.id,))}
    return val
